#!/bin/bash

# LLM Training Data Generator Runner Script
# This script provides easy ways to run the data generator with different configurations

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR_SCRIPT="$SCRIPT_DIR/llm_training_data_generator.py"
DEFAULT_BATCH_SIZE=100
DEFAULT_OUTPUT_DIR="training_data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check if Python 3 is available
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null && python -c "import sys; exit(0 if sys.version_info[0] >= 3 else 1)" 2>/dev/null; then
        PYTHON_CMD="python"
    else
        error "Python 3 is required but not found. Please install Python 3.7 or higher."
        exit 1
    fi
    
    info "Using Python: $($PYTHON_CMD --version)"
}

# Check if the generator script exists
check_script() {
    if [[ ! -f "$GENERATOR_SCRIPT" ]]; then
        error "Generator script not found at: $GENERATOR_SCRIPT"
        exit 1
    fi
}

# Display usage information
usage() {
    cat << EOF
LLM Training Data Generator Runner

Usage: $0 [COMMAND] [OPTIONS]

Commands:
    generate        Generate a single batch of training data (default)
    continuous      Run in continuous mode with periodic generation
    test           Generate a small test batch (10 examples)
    help           Show this help message

Options:
    -b, --batch-size SIZE    Number of examples to generate (default: $DEFAULT_BATCH_SIZE)
    -o, --output-dir DIR     Output directory (default: $DEFAULT_OUTPUT_DIR)
    -f, --filename FILE      Output filename (optional)
    -i, --interval SECONDS   Interval for continuous mode in seconds (default: 3600)
    -v, --verbose           Enable verbose logging

Examples:
    $0 generate                          # Generate 100 examples
    $0 generate -b 50                    # Generate 50 examples
    $0 continuous -i 1800                # Run continuously with 30min intervals
    $0 test                              # Generate 10 test examples
    $0 generate -o custom_data -f my_data.json  # Custom output location

EOF
}

# Generate a single batch
generate_batch() {
    local batch_size="$1"
    local output_dir="$2"
    local filename="$3"
    local verbose="$4"
    
    log "Starting single batch generation..."
    info "Batch size: $batch_size"
    info "Output directory: $output_dir"
    
    local cmd="$PYTHON_CMD $GENERATOR_SCRIPT --batch-size $batch_size --output-dir $output_dir"
    
    if [[ -n "$filename" ]]; then
        cmd="$cmd --filename $filename"
        info "Output filename: $filename"
    fi
    
    if [[ "$verbose" == "true" ]]; then
        info "Running command: $cmd"
    fi
    
    if $cmd; then
        log "✅ Batch generation completed successfully!"
    else
        error "❌ Batch generation failed!"
        exit 1
    fi
}

# Run in continuous mode
run_continuous() {
    local batch_size="$1"
    local output_dir="$2"
    local interval="$3"
    local verbose="$4"
    
    log "Starting continuous generation mode..."
    info "Batch size: $batch_size"
    info "Output directory: $output_dir"
    info "Interval: ${interval}s ($(($interval / 60)) minutes)"
    
    local cmd="$PYTHON_CMD $GENERATOR_SCRIPT --continuous --batch-size $batch_size --output-dir $output_dir --interval $interval"
    
    if [[ "$verbose" == "true" ]]; then
        info "Running command: $cmd"
    fi
    
    warning "Press Ctrl+C to stop continuous generation"
    
    # Set up signal handlers for graceful shutdown
    trap 'log "Stopping continuous generation..."; exit 0' INT TERM
    
    if $cmd; then
        log "Continuous generation stopped"
    else
        error "Continuous generation failed!"
        exit 1
    fi
}

# Generate test batch
generate_test() {
    local output_dir="$1"
    local verbose="$2"
    
    log "Generating test batch (10 examples)..."
    generate_batch 10 "$output_dir" "test_data.json" "$verbose"
}

# Create output directory if it doesn't exist
ensure_output_dir() {
    local output_dir="$1"
    
    if [[ ! -d "$output_dir" ]]; then
        info "Creating output directory: $output_dir"
        mkdir -p "$output_dir"
    fi
}

# Main function
main() {
    local command="generate"
    local batch_size="$DEFAULT_BATCH_SIZE"
    local output_dir="$DEFAULT_OUTPUT_DIR"
    local filename=""
    local interval="3600"
    local verbose="false"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            generate|continuous|test|help)
                command="$1"
                shift
                ;;
            -b|--batch-size)
                batch_size="$2"
                shift 2
                ;;
            -o|--output-dir)
                output_dir="$2"
                shift 2
                ;;
            -f|--filename)
                filename="$2"
                shift 2
                ;;
            -i|--interval)
                interval="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose="true"
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
    
    # Validate batch size
    if ! [[ "$batch_size" =~ ^[0-9]+$ ]] || [[ "$batch_size" -lt 1 ]]; then
        error "Invalid batch size: $batch_size (must be a positive integer)"
        exit 1
    fi
    
    # Validate interval
    if ! [[ "$interval" =~ ^[0-9]+$ ]] || [[ "$interval" -lt 60 ]]; then
        error "Invalid interval: $interval (must be at least 60 seconds)"
        exit 1
    fi
    
    # Run pre-checks
    check_python
    check_script
    ensure_output_dir "$output_dir"
    
    # Execute command
    case $command in
        generate)
            generate_batch "$batch_size" "$output_dir" "$filename" "$verbose"
            ;;
        continuous)
            run_continuous "$batch_size" "$output_dir" "$interval" "$verbose"
            ;;
        test)
            generate_test "$output_dir" "$verbose"
            ;;
        help)
            usage
            ;;
        *)
            error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Check if script is being run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi