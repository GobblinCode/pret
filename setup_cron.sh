#!/bin/bash

# Setup Cron Jobs for LLM Training Data Generator
# This script sets up automated cron jobs for continuous data generation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER_SCRIPT="$SCRIPT_DIR/run_data_generator.sh"
CRON_LOG_DIR="$SCRIPT_DIR/logs"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Check if cron is available
check_cron() {
    if ! command -v crontab &> /dev/null; then
        error "crontab command not found. Please install cron."
        exit 1
    fi
    
    if ! systemctl is-active --quiet cron 2>/dev/null && ! systemctl is-active --quiet crond 2>/dev/null; then
        warning "Cron service may not be running. You may need to start it manually."
    fi
}

# Create log directory
setup_logging() {
    mkdir -p "$CRON_LOG_DIR"
    log "Created log directory: $CRON_LOG_DIR"
}

# Make runner script executable
setup_permissions() {
    chmod +x "$RUNNER_SCRIPT"
    log "Made runner script executable: $RUNNER_SCRIPT"
}

# Display current cron jobs
show_current_cron() {
    log "Current cron jobs:"
    crontab -l 2>/dev/null | grep -E "(data_generator|training_data)" || echo "  No existing data generator cron jobs found"
}

# Add cron job
add_cron_job() {
    local schedule="$1"
    local command="$2"
    local description="$3"
    
    # Get current crontab
    local temp_cron=$(mktemp)
    crontab -l 2>/dev/null > "$temp_cron" || true
    
    # Check if job already exists
    if grep -q "$command" "$temp_cron"; then
        warning "Cron job already exists: $description"
        rm "$temp_cron"
        return 1
    fi
    
    # Add new job
    echo "# $description" >> "$temp_cron"
    echo "$schedule $command" >> "$temp_cron"
    echo "" >> "$temp_cron"
    
    # Install new crontab
    crontab "$temp_cron"
    rm "$temp_cron"
    
    log "Added cron job: $description"
    return 0
}

# Remove existing data generator cron jobs
remove_existing_jobs() {
    local temp_cron=$(mktemp)
    crontab -l 2>/dev/null | grep -v -E "(data_generator|training_data|LLM Training)" > "$temp_cron" || true
    crontab "$temp_cron"
    rm "$temp_cron"
    log "Removed existing data generator cron jobs"
}

# Setup predefined schedules
setup_hourly() {
    local log_file="$CRON_LOG_DIR/hourly_generation.log"
    local command="$RUNNER_SCRIPT generate -b 50 >> $log_file 2>&1"
    add_cron_job "0 * * * *" "$command" "LLM Training Data - Hourly Generation (50 examples)"
}

setup_daily() {
    local log_file="$CRON_LOG_DIR/daily_generation.log"
    local command="$RUNNER_SCRIPT generate -b 200 >> $log_file 2>&1"
    add_cron_job "0 2 * * *" "$command" "LLM Training Data - Daily Generation (200 examples at 2 AM)"
}

setup_weekly() {
    local log_file="$CRON_LOG_DIR/weekly_generation.log"
    local command="$RUNNER_SCRIPT generate -b 500 >> $log_file 2>&1"
    add_cron_job "0 3 * * 0" "$command" "LLM Training Data - Weekly Generation (500 examples on Sunday at 3 AM)"
}

setup_cleanup() {
    local log_file="$CRON_LOG_DIR/cleanup.log"
    local command="find $SCRIPT_DIR/training_data -name '*.json' -mtime +30 -delete >> $log_file 2>&1"
    add_cron_job "0 1 * * 0" "$command" "LLM Training Data - Weekly Cleanup (remove files older than 30 days)"
}

# Interactive setup
interactive_setup() {
    echo "LLM Training Data Generator - Cron Setup"
    echo "======================================="
    echo
    echo "Available schedules:"
    echo "1. Hourly (50 examples every hour)"
    echo "2. Daily (200 examples at 2 AM daily)"
    echo "3. Weekly (500 examples on Sunday at 3 AM)"
    echo "4. Custom schedule"
    echo "5. Remove all existing jobs"
    echo "6. Show current jobs only"
    echo
    
    read -p "Select an option (1-6): " choice
    
    case $choice in
        1)
            setup_hourly
            setup_cleanup
            ;;
        2)
            setup_daily
            setup_cleanup
            ;;
        3)
            setup_weekly
            setup_cleanup
            ;;
        4)
            echo
            echo "Custom schedule format: minute hour day month weekday"
            echo "Examples:"
            echo "  '*/30 * * * *' = Every 30 minutes"
            echo "  '0 */6 * * *' = Every 6 hours"
            echo "  '0 9 * * 1-5' = 9 AM on weekdays"
            echo
            read -p "Enter cron schedule: " custom_schedule
            read -p "Enter batch size (default 100): " batch_size
            batch_size=${batch_size:-100}
            
            local log_file="$CRON_LOG_DIR/custom_generation.log"
            local command="$RUNNER_SCRIPT generate -b $batch_size >> $log_file 2>&1"
            add_cron_job "$custom_schedule" "$command" "LLM Training Data - Custom Generation ($batch_size examples)"
            setup_cleanup
            ;;
        5)
            remove_existing_jobs
            ;;
        6)
            show_current_cron
            exit 0
            ;;
        *)
            error "Invalid option: $choice"
            exit 1
            ;;
    esac
}

# Command line setup
command_line_setup() {
    local schedule="$1"
    
    case $schedule in
        hourly)
            setup_hourly
            setup_cleanup
            ;;
        daily)
            setup_daily
            setup_cleanup
            ;;
        weekly)
            setup_weekly
            setup_cleanup
            ;;
        remove)
            remove_existing_jobs
            ;;
        show)
            show_current_cron
            exit 0
            ;;
        *)
            error "Invalid schedule: $schedule"
            echo "Valid options: hourly, daily, weekly, remove, show"
            exit 1
            ;;
    esac
}

# Display usage
usage() {
    cat << EOF
LLM Training Data Generator - Cron Setup

Usage: $0 [SCHEDULE]

Schedules:
    hourly      Generate 50 examples every hour
    daily       Generate 200 examples daily at 2 AM
    weekly      Generate 500 examples weekly on Sunday at 3 AM
    remove      Remove all existing data generator cron jobs
    show        Show current cron jobs
    
If no schedule is provided, interactive mode will be used.

Examples:
    $0              # Interactive setup
    $0 daily        # Setup daily generation
    $0 show         # Show current jobs
    $0 remove       # Remove all jobs

EOF
}

# Main function
main() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
        exit 0
    fi
    
    log "Setting up LLM Training Data Generator cron jobs..."
    
    # Pre-checks
    check_cron
    setup_logging
    setup_permissions
    
    echo
    show_current_cron
    echo
    
    if [[ $# -eq 0 ]]; then
        # Interactive mode
        interactive_setup
    else
        # Command line mode
        command_line_setup "$1"
    fi
    
    echo
    log "Cron setup completed!"
    echo
    show_current_cron
    echo
    log "Log files will be stored in: $CRON_LOG_DIR"
    log "To monitor generation: tail -f $CRON_LOG_DIR/*.log"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi