# LLM Training Data Generator

A comprehensive system for automatically generating high-quality training data for continuous LLM learning and improvement, specifically tailored for gambling review websites and affiliate marketing content.

## 🚀 Features

### Core Capabilities
- **Diverse Content Generation**: Reviews, Q&A pairs, SEO articles, comparisons, and user interactions
- **Quality Validation**: Built-in filtering and quality scoring system
- **Automated Scheduling**: Cron job setup for continuous data generation
- **Configurable Parameters**: JSON-based configuration for easy customization
- **Comprehensive Logging**: Detailed logging and monitoring capabilities

### Content Types Generated
1. **Gambling Site Reviews** - Comprehensive reviews with ratings, pros/cons, and detailed analysis
2. **Comparison Articles** - Head-to-head comparisons between gambling sites
3. **Q&A Pairs** - Customer support scenarios and informational content
4. **SEO-Optimized Articles** - Keyword-rich content for search engine optimization
5. **User Interactions** - Realistic customer support conversations

## 📁 File Structure

```
├── llm_training_data_generator.py  # Main data generation script
├── run_data_generator.sh          # Convenient runner script
├── setup_cron.sh                  # Automated cron job setup
├── config.json                    # Configuration file
├── requirements.txt               # Python dependencies
├── DATA_GENERATOR_README.md       # This file
├── training_data/                 # Generated data output directory
└── logs/                         # Log files directory
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Linux/Unix environment with bash
- Cron service (for automation)

### Quick Start

1. **Make scripts executable**:
```bash
chmod +x run_data_generator.sh
chmod +x setup_cron.sh
```

2. **Generate test data**:
```bash
./run_data_generator.sh test
```

3. **Generate a full batch**:
```bash
./run_data_generator.sh generate
```

4. **Set up automated generation**:
```bash
./setup_cron.sh daily
```

## 📖 Usage Guide

### Manual Generation

#### Basic Usage
```bash
# Generate 100 examples (default)
./run_data_generator.sh generate

# Generate specific number of examples
./run_data_generator.sh generate -b 50

# Generate with custom output location
./run_data_generator.sh generate -o custom_data -f my_data.json
```

#### Continuous Mode
```bash
# Run continuously with 1-hour intervals
./run_data_generator.sh continuous

# Custom interval (30 minutes)
./run_data_generator.sh continuous -i 1800
```

#### Direct Python Usage
```bash
# Basic generation
python3 llm_training_data_generator.py --batch-size 100

# Continuous mode
python3 llm_training_data_generator.py --continuous --interval 3600

# Custom output directory
python3 llm_training_data_generator.py --output-dir custom_data
```

### Automated Generation

#### Set Up Cron Jobs
```bash
# Interactive setup
./setup_cron.sh

# Quick daily setup
./setup_cron.sh daily

# Hourly generation
./setup_cron.sh hourly

# Weekly generation
./setup_cron.sh weekly
```

#### Predefined Schedules
- **Hourly**: 50 examples every hour
- **Daily**: 200 examples at 2 AM daily
- **Weekly**: 500 examples on Sunday at 3 AM

#### Manage Cron Jobs
```bash
# Show current jobs
./setup_cron.sh show

# Remove all data generator jobs
./setup_cron.sh remove
```

## ⚙️ Configuration

### Main Configuration File (`config.json`)

The system uses a comprehensive JSON configuration file that allows you to customize:

#### Generation Settings
```json
{
  "generation_settings": {
    "default_batch_size": 100,
    "output_directory": "training_data",
    "continuous_interval_seconds": 3600,
    "quality_threshold": 0.6
  }
}
```

#### Content Distribution
Control the mix of content types:
```json
{
  "content_distribution": {
    "reviews": 0.3,        # 30% reviews
    "qa_pairs": 0.25,      # 25% Q&A pairs
    "seo_content": 0.2,    # 20% SEO articles
    "comparisons": 0.15,   # 15% comparisons
    "interactions": 0.1    # 10% interactions
  }
}
```

#### Gambling Sites Database
Add or modify gambling sites:
```json
{
  "gambling_sites": {
    "new_site": {
      "name": "New Casino",
      "bonus": "200% up to $2,000",
      "features": ["Slots", "Live Dealer"],
      "pros": ["Great bonuses", "Fast payouts"],
      "cons": ["Limited games"],
      "rating": 85,
      "active": true
    }
  }
}
```

### Environment Variables
You can also use environment variables to override settings:
```bash
export DATA_GENERATOR_BATCH_SIZE=150
export DATA_GENERATOR_OUTPUT_DIR="/custom/path"
export DATA_GENERATOR_QUALITY_THRESHOLD=0.7
```

## 📊 Output Format

### Training Data Structure
Generated data is saved in JSON format with the following structure:
```json
{
  "metadata": {
    "generated_at": "2024-01-15T10:30:00",
    "total_examples": 100,
    "generator_version": "1.0.0"
  },
  "examples": [
    {
      "id": "abc123def456",
      "type": "comprehensive_review",
      "input_text": "Write a comprehensive review of Bovada gambling site",
      "output_text": "# Bovada Review - 92/100\n\n## Overview\n...",
      "metadata": {
        "site": "bovada",
        "rating": 92,
        "word_count": 245
      },
      "quality_score": 0.89,
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### File Naming Convention
- Manual generation: `training_data_YYYYMMDD_HHMMSS.json`
- Custom filename: As specified
- Test generation: `test_data.json`

## 🔍 Quality Control

### Quality Scoring System
Each example is automatically scored based on:
- **Length appropriateness** (100-2000 characters)
- **Keyword relevance** (gambling-related terms)
- **Structure quality** (formatting, lists, etc.)
- **Content safety** (no harmful patterns)

### Quality Filters
- Minimum input/output length requirements
- Harmful content detection and removal
- Keyword relevance checking
- Duplicate content prevention

### Validation Process
1. Content generation
2. Quality scoring
3. Safety filtering
4. Validation checks
5. Final output

## 📈 Monitoring & Logging

### Log Files
- `data_generation.log` - Main application log
- `logs/hourly_generation.log` - Hourly cron job logs
- `logs/daily_generation.log` - Daily cron job logs
- `logs/weekly_generation.log` - Weekly cron job logs
- `logs/cleanup.log` - File cleanup logs

### Monitoring Commands
```bash
# Monitor real-time generation
tail -f data_generation.log

# Monitor cron job execution
tail -f logs/daily_generation.log

# Check generation statistics
grep "Generated.*valid examples" data_generation.log
```

### Performance Metrics
The system tracks:
- Examples generated per batch
- Quality score distribution
- Generation time per batch
- Validation success rate
- Content type distribution

## 🔧 Customization

### Adding New Content Types

1. **Create a new generator class**:
```python
class NewContentGenerator(GamblingDataGenerator):
    def generate_new_content(self) -> TrainingExample:
        # Implementation here
        pass
```

2. **Update the TrainingDataManager**:
```python
# Add to generate_batch method
elif example_type == "new_content":
    for _ in range(count):
        example = self.new_generator.generate_new_content()
        examples.append(example)
```

3. **Update configuration**:
```json
{
  "content_distribution": {
    "new_content": 0.1
  }
}
```

### Adding New Gambling Sites

Edit `config.json`:
```json
{
  "gambling_sites": {
    "your_site": {
      "name": "Your Site Name",
      "bonus": "Bonus description",
      "features": ["Feature 1", "Feature 2"],
      "pros": ["Pro 1", "Pro 2"],
      "cons": ["Con 1", "Con 2"],
      "rating": 85,
      "active": true
    }
  }
}
```

### Custom Q&A Categories

Add new categories in `config.json`:
```json
{
  "qa_categories": {
    "new_category": {
      "weight": 0.1,
      "templates": [
        {
          "question": "Your question?",
          "answer": "Your answer."
        }
      ]
    }
  }
}
```

## 🚨 Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Check Python installation
python3 --version
# or
python --version

# Install Python 3 if missing (Ubuntu/Debian)
sudo apt-get install python3
```

#### Permission Denied
```bash
# Make scripts executable
chmod +x run_data_generator.sh setup_cron.sh
```

#### Cron Jobs Not Running
```bash
# Check cron service
sudo systemctl status cron

# Start cron service
sudo systemctl start cron

# Check cron logs
sudo tail -f /var/log/cron
```

#### Low Quality Scores
- Adjust quality threshold in `config.json`
- Review harmful patterns list
- Check keyword requirements

#### Output Directory Issues
```bash
# Create directory manually
mkdir -p training_data

# Check permissions
ls -la training_data
```

### Debug Mode
Enable verbose logging:
```bash
./run_data_generator.sh generate -v
```

## 📋 Best Practices

### Generation Frequency
- **Development**: Use test mode frequently
- **Production**: Daily or weekly generation recommended
- **High-volume**: Hourly generation with smaller batches

### File Management
- Set up automatic cleanup (included in cron setup)
- Monitor disk space usage
- Archive old training data regularly

### Quality Monitoring
- Review quality scores regularly
- Adjust thresholds based on requirements
- Monitor for content drift

### Security Considerations
- Review generated content for compliance
- Ensure responsible gambling messaging
- Validate affiliate link accuracy

## 🔄 Maintenance

### Regular Tasks
1. **Monitor generation logs** for errors
2. **Review quality scores** and adjust thresholds
3. **Update gambling site data** in config
4. **Clean up old files** (automated)
5. **Check disk space** usage

### Updates and Improvements
1. **Backup configuration** before changes
2. **Test changes** with small batches
3. **Monitor impact** on quality scores
4. **Document modifications**

## 📞 Support

### Getting Help
1. Check logs for error messages
2. Review this documentation
3. Test with small batches first
4. Verify configuration syntax

### Contributing
- Report bugs or issues
- Suggest new content types
- Share configuration improvements
- Contribute to documentation

## 🎯 Advanced Usage

### Batch Processing
```bash
# Generate multiple batches
for i in {1..5}; do
  ./run_data_generator.sh generate -b 50 -f "batch_$i.json"
  sleep 60
done
```

### Custom Scheduling
```bash
# Every 2 hours during business hours (9 AM - 5 PM)
0 9-17/2 * * * /path/to/run_data_generator.sh generate -b 25

# Weekdays only at 10 AM
0 10 * * 1-5 /path/to/run_data_generator.sh generate -b 100
```

### Integration with Other Systems
The generated JSON data can be easily integrated with:
- Machine learning pipelines
- Data processing workflows
- Content management systems
- API endpoints

---

**Happy Data Generation!** 🎰

For additional support or questions, ensure you're following all applicable laws and regulations regarding gambling content and affiliate marketing in your jurisdiction.