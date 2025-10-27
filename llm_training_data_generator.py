#!/usr/bin/env python3
"""
LLM Training Data Generator for Gambling Review Website

This script automatically generates high-quality training data for continuous 
LLM learning and improvement. It creates diverse datasets including:
- Gambling site reviews and comparisons
- Q&A pairs for customer support
- SEO-optimized content
- User interaction simulations
- Affiliate marketing content
"""

import json
import random
import datetime
import os
import re
import hashlib
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TrainingExample:
    """Structure for a training example"""
    id: str
    type: str
    input_text: str
    output_text: str
    metadata: Dict[str, Any]
    quality_score: float
    created_at: str

class GamblingDataGenerator:
    """Main class for generating gambling-related training data"""
    
    def __init__(self, output_dir: str = "training_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Gambling sites database
        self.gambling_sites = {
            "bovada": {
                "name": "Bovada",
                "bonus": "100% up to $1,000",
                "features": ["Sports Betting", "Casino Games", "Poker", "Live Dealer"],
                "pros": ["Excellent mobile app", "Fast payouts", "Great customer service"],
                "cons": ["Limited banking options", "No phone support"],
                "rating": 92
            },
            "ignition": {
                "name": "Ignition Casino",
                "bonus": "150% up to $1,500",
                "features": ["Slots", "Table Games", "Live Dealer", "Tournaments"],
                "pros": ["Anonymous play", "Crypto-friendly", "High-quality games"],
                "cons": ["Limited customer support hours", "Withdrawal fees"],
                "rating": 88
            },
            "draftkings": {
                "name": "DraftKings",
                "bonus": "$1,000 No Sweat First Bet",
                "features": ["Sports Betting", "Daily Fantasy", "Casino", "Live Betting"],
                "pros": ["Legal in many states", "Excellent odds", "Great promotions"],
                "cons": ["Geographic restrictions", "Account verification required"],
                "rating": 95
            },
            "fanduel": {
                "name": "FanDuel",
                "bonus": "Bet $5, Get $150 in Bonus Bets",
                "features": ["Sports Betting", "Casino", "Racing", "Daily Fantasy"],
                "pros": ["User-friendly interface", "Fast deposits", "Live streaming"],
                "cons": ["Limited international access", "Lower betting limits"],
                "rating": 93
            }
        }
        
        # Content templates and patterns
        self.review_templates = [
            "comprehensive_review",
            "quick_overview",
            "comparison_focused",
            "bonus_focused",
            "mobile_focused"
        ]
        
        self.question_categories = [
            "account_setup",
            "bonuses_promotions",
            "banking_payments",
            "game_rules",
            "technical_support",
            "responsible_gambling",
            "legal_regulatory"
        ]
        
    def generate_id(self, content: str) -> str:
        """Generate unique ID for training example"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def calculate_quality_score(self, text: str, metadata: Dict) -> float:
        """Calculate quality score for training example"""
        score = 0.8  # Base score
        
        # Length bonus
        if 100 <= len(text) <= 2000:
            score += 0.1
        
        # Keyword relevance
        gambling_keywords = ["casino", "betting", "bonus", "odds", "payout", "review"]
        keyword_count = sum(1 for keyword in gambling_keywords if keyword.lower() in text.lower())
        score += min(keyword_count * 0.02, 0.1)
        
        # Structure bonus
        if any(marker in text for marker in ["1.", "2.", "•", "-"]):
            score += 0.05
        
        return min(score, 1.0)

class ReviewGenerator(GamblingDataGenerator):
    """Generates gambling site review content"""
    
    def generate_comprehensive_review(self, site_key: str) -> TrainingExample:
        """Generate a comprehensive review"""
        site = self.gambling_sites[site_key]
        
        input_text = f"Write a comprehensive review of {site['name']} gambling site"
        
        output_text = f"""# {site['name']} Review - {site['rating']}/100

## Overview
{site['name']} is a {'premium' if site['rating'] > 90 else 'solid'} online gambling platform offering {', '.join(site['features'][:3])}. With a current rating of {site['rating']}/100, it stands out for its {'exceptional' if site['rating'] > 90 else 'reliable'} service.

## Welcome Bonus
New players can claim {site['bonus']} - one of the {'most generous' if 'up to $1,000' in site['bonus'] or 'up to $1,500' in site['bonus'] else 'competitive'} offers in the industry.

## Key Features
{chr(10).join(f"• {feature}" for feature in site['features'])}

## Pros
{chr(10).join(f"✓ {pro}" for pro in site['pros'])}

## Cons  
{chr(10).join(f"✗ {con}" for con in site['cons'])}

## Final Verdict
{site['name']} {'exceeds expectations' if site['rating'] > 90 else 'meets industry standards'} with its {'outstanding' if site['rating'] > 90 else 'solid'} platform. The {site['bonus']} welcome bonus and {site['features'][0].lower()} options make it {'a top choice' if site['rating'] > 90 else 'worth considering'} for both new and experienced players.

**Rating: {site['rating']}/100**"""

        return TrainingExample(
            id=self.generate_id(input_text + output_text),
            type="comprehensive_review",
            input_text=input_text,
            output_text=output_text,
            metadata={
                "site": site_key,
                "rating": site['rating'],
                "word_count": len(output_text.split())
            },
            quality_score=self.calculate_quality_score(output_text, {}),
            created_at=datetime.datetime.now().isoformat()
        )
    
    def generate_comparison_review(self, site1_key: str, site2_key: str) -> TrainingExample:
        """Generate a comparison between two sites"""
        site1 = self.gambling_sites[site1_key]
        site2 = self.gambling_sites[site2_key]
        
        input_text = f"Compare {site1['name']} vs {site2['name']} gambling sites"
        
        winner = site1 if site1['rating'] > site2['rating'] else site2
        winner_key = site1_key if site1['rating'] > site2['rating'] else site2_key
        
        output_text = f"""# {site1['name']} vs {site2['name']} - Head-to-Head Comparison

## Quick Comparison
| Feature | {site1['name']} | {site2['name']} |
|---------|----------|----------|
| Rating | {site1['rating']}/100 | {site2['rating']}/100 |
| Bonus | {site1['bonus']} | {site2['bonus']} |
| Key Features | {len(site1['features'])} features | {len(site2['features'])} features |

## Detailed Analysis

### Welcome Bonuses
- **{site1['name']}**: {site1['bonus']}
- **{site2['name']}**: {site2['bonus']}

### Game Selection
- **{site1['name']}**: {', '.join(site1['features'])}
- **{site2['name']}**: {', '.join(site2['features'])}

### Strengths & Weaknesses

**{site1['name']} Pros:**
{chr(10).join(f"• {pro}" for pro in site1['pros'])}

**{site1['name']} Cons:**
{chr(10).join(f"• {con}" for con in site1['cons'])}

**{site2['name']} Pros:**
{chr(10).join(f"• {pro}" for pro in site2['pros'])}

**{site2['name']} Cons:**
{chr(10).join(f"• {con}" for con in site2['cons'])}

## The Verdict
{winner['name']} takes the lead with a {winner['rating']}/100 rating. {'It excels in' if winner['rating'] > 90 else 'It performs well in'} {winner['pros'][0].lower()} and offers {winner['bonus']}.

**Winner: {winner['name']}** 🏆"""

        return TrainingExample(
            id=self.generate_id(input_text + output_text),
            type="comparison_review",
            input_text=input_text,
            output_text=output_text,
            metadata={
                "sites": [site1_key, site2_key],
                "winner": winner_key,
                "word_count": len(output_text.split())
            },
            quality_score=self.calculate_quality_score(output_text, {}),
            created_at=datetime.datetime.now().isoformat()
        )

class QAGenerator(GamblingDataGenerator):
    """Generates Q&A pairs for customer support and information"""
    
    def __init__(self, output_dir: str = "training_data"):
        super().__init__(output_dir)
        
        self.qa_templates = {
            "account_setup": [
                ("How do I create an account?", "To create an account, click 'Sign Up', provide your email, create a password, and verify your identity with required documents."),
                ("What documents do I need for verification?", "You'll need a government-issued ID (driver's license or passport) and a recent utility bill or bank statement for address verification."),
                ("How long does account verification take?", "Account verification typically takes 24-48 hours. You'll receive an email confirmation once approved.")
            ],
            "bonuses_promotions": [
                ("How do I claim my welcome bonus?", "Make your first deposit and the bonus will be automatically credited to your account. Some bonuses require a promo code during deposit."),
                ("What are the wagering requirements?", "Most bonuses have 25x-40x wagering requirements. This means you must bet the bonus amount 25-40 times before withdrawing."),
                ("Can I withdraw my bonus immediately?", "No, bonuses must meet wagering requirements first. Only the winnings from bonus play can be withdrawn after meeting requirements.")
            ],
            "banking_payments": [
                ("What payment methods do you accept?", "We accept credit/debit cards, bank transfers, e-wallets (PayPal, Skrill), and cryptocurrencies (Bitcoin, Ethereum)."),
                ("How long do withdrawals take?", "E-wallet withdrawals: 24-48 hours, Bank transfers: 3-5 business days, Crypto: 1-24 hours."),
                ("Are there withdrawal fees?", "Most withdrawals are free, but some methods may have small processing fees. Check the banking section for specific fees.")
            ]
        }
    
    def generate_qa_pair(self, category: str) -> TrainingExample:
        """Generate a Q&A pair for a specific category"""
        if category not in self.qa_templates:
            category = random.choice(list(self.qa_templates.keys()))
        
        question, answer = random.choice(self.qa_templates[category])
        
        return TrainingExample(
            id=self.generate_id(question + answer),
            type="qa_pair",
            input_text=question,
            output_text=answer,
            metadata={
                "category": category,
                "word_count": len(answer.split())
            },
            quality_score=self.calculate_quality_score(answer, {"category": category}),
            created_at=datetime.datetime.now().isoformat()
        )

class SEOContentGenerator(GamblingDataGenerator):
    """Generates SEO-optimized content"""
    
    def generate_seo_article(self, topic: str) -> TrainingExample:
        """Generate SEO-optimized article"""
        topics = {
            "best_gambling_sites": {
                "title": "Best Online Gambling Sites 2024 - Top Rated Casinos",
                "keywords": ["best gambling sites", "online casinos", "top rated"],
                "content_outline": ["Introduction", "Top 5 Sites", "How We Rate", "Conclusion"]
            },
            "gambling_bonuses": {
                "title": "Best Casino Bonuses 2024 - Welcome Offers & Free Spins",
                "keywords": ["casino bonuses", "welcome bonus", "free spins"],
                "content_outline": ["Types of Bonuses", "Best Current Offers", "Terms to Know", "How to Claim"]
            }
        }
        
        if topic not in topics:
            topic = random.choice(list(topics.keys()))
        
        topic_data = topics[topic]
        input_text = f"Write an SEO article about {topic.replace('_', ' ')}"
        
        output_text = f"""# {topic_data['title']}

## Introduction
Finding the {topic_data['keywords'][0]} can be challenging with so many options available. Our expert team has reviewed hundreds of platforms to bring you this comprehensive guide.

## Key Factors We Consider
- **Security & Licensing**: All recommended sites are fully licensed
- **Game Selection**: Variety and quality of available games  
- **Bonuses & Promotions**: Value and fairness of offers
- **Payment Options**: Speed and reliability of transactions
- **Customer Support**: Availability and helpfulness

## Top Recommendations

### 1. Bovada - 92/100
- **Bonus**: 100% up to $1,000
- **Best For**: Sports betting and casino games
- **Highlights**: Fast payouts, mobile-friendly

### 2. DraftKings - 95/100  
- **Bonus**: $1,000 No Sweat First Bet
- **Best For**: Legal sports betting
- **Highlights**: Excellent odds, great app

### 3. Ignition Casino - 88/100
- **Bonus**: 150% up to $1,500
- **Best For**: Anonymous play
- **Highlights**: Crypto-friendly, tournaments

## How to Get Started
1. Choose a licensed site from our recommendations
2. Create your account with valid information
3. Make your first deposit to claim bonuses
4. Start playing responsibly

## Conclusion
The {topic_data['keywords'][0]} offer secure, entertaining experiences with generous bonuses. Always gamble responsibly and within your means.

*Last updated: {datetime.datetime.now().strftime('%B %Y')}*"""

        return TrainingExample(
            id=self.generate_id(input_text + output_text),
            type="seo_article",
            input_text=input_text,
            output_text=output_text,
            metadata={
                "topic": topic,
                "keywords": topic_data['keywords'],
                "word_count": len(output_text.split()),
                "seo_optimized": True
            },
            quality_score=self.calculate_quality_score(output_text, {"seo": True}),
            created_at=datetime.datetime.now().isoformat()
        )

class UserInteractionSimulator(GamblingDataGenerator):
    """Simulates realistic user interactions and conversations"""
    
    def generate_customer_support_conversation(self) -> TrainingExample:
        """Generate a realistic customer support conversation"""
        scenarios = [
            {
                "issue": "withdrawal_delay",
                "user_messages": [
                    "Hi, I requested a withdrawal 3 days ago but haven't received it yet. Can you help?",
                    "I used my Visa card for the deposit. The withdrawal was for $500.",
                    "Okay, I understand. How much longer should I expect to wait?"
                ],
                "support_responses": [
                    "I'd be happy to help you with your withdrawal. Can you please tell me which payment method you used for the withdrawal and the amount?",
                    "Thank you for that information. Visa withdrawals typically take 3-5 business days to process. Since you're on day 3, it should appear in your account within the next 1-2 business days.",
                    "You should see the funds in your account by tomorrow or the day after. If you don't receive it by then, please contact us again and we'll investigate further. Is there anything else I can help you with today?"
                ]
            },
            {
                "issue": "bonus_question",
                "user_messages": [
                    "I just signed up and made my first deposit. Where is my welcome bonus?",
                    "I deposited $200 and used the code WELCOME100.",
                    "Great, thank you! When can I withdraw the bonus?"
                ],
                "support_responses": [
                    "Welcome to our casino! I can help you with your bonus. Can you tell me how much you deposited and if you used a bonus code?",
                    "Perfect! I can see your deposit and the WELCOME100 code was applied correctly. Your 100% bonus of $200 has been added to your bonus balance. You can see it in your account under 'Bonus Funds'.",
                    "The bonus has a 30x wagering requirement, which means you need to wager $6,000 ($200 × 30) before you can withdraw it. You can track your progress in the 'My Bonuses' section of your account."
                ]
            }
        ]
        
        scenario = random.choice(scenarios)
        
        # Create conversation format
        conversation = []
        for i, (user_msg, support_msg) in enumerate(zip(scenario["user_messages"], scenario["support_responses"])):
            conversation.append(f"User: {user_msg}")
            conversation.append(f"Support: {support_msg}")
        
        input_text = f"Handle a customer support conversation about {scenario['issue'].replace('_', ' ')}"
        output_text = "\n\n".join(conversation)
        
        return TrainingExample(
            id=self.generate_id(input_text + output_text),
            type="customer_support",
            input_text=input_text,
            output_text=output_text,
            metadata={
                "scenario": scenario["issue"],
                "message_count": len(scenario["user_messages"]) + len(scenario["support_responses"]),
                "conversation_type": "support"
            },
            quality_score=self.calculate_quality_score(output_text, {"conversation": True}),
            created_at=datetime.datetime.now().isoformat()
        )

class DataQualityValidator:
    """Validates and filters training data for quality"""
    
    @staticmethod
    def validate_example(example: TrainingExample) -> Tuple[bool, List[str]]:
        """Validate a training example and return issues if any"""
        issues = []
        
        # Check minimum length
        if len(example.input_text) < 10:
            issues.append("Input text too short")
        
        if len(example.output_text) < 20:
            issues.append("Output text too short")
        
        # Check for harmful content
        harmful_patterns = [
            r'\b(hack|cheat|exploit)\b',
            r'\bguaranteed\s+win\b',
            r'\brisk\s+free\b'
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, example.output_text, re.IGNORECASE):
                issues.append(f"Contains potentially harmful content: {pattern}")
        
        # Check quality score
        if example.quality_score < 0.6:
            issues.append("Quality score too low")
        
        return len(issues) == 0, issues

class TrainingDataManager:
    """Manages the complete training data generation process"""
    
    def __init__(self, output_dir: str = "training_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize generators
        self.review_generator = ReviewGenerator(output_dir)
        self.qa_generator = QAGenerator(output_dir)
        self.seo_generator = SEOContentGenerator(output_dir)
        self.interaction_simulator = UserInteractionSimulator(output_dir)
        self.validator = DataQualityValidator()
        
        self.generated_examples = []
    
    def generate_batch(self, batch_size: int = 100) -> List[TrainingExample]:
        """Generate a batch of training examples"""
        examples = []
        
        # Distribution of example types
        type_distribution = {
            "reviews": 0.3,
            "qa_pairs": 0.25,
            "seo_content": 0.2,
            "comparisons": 0.15,
            "interactions": 0.1
        }
        
        for example_type, ratio in type_distribution.items():
            count = int(batch_size * ratio)
            
            if example_type == "reviews":
                for _ in range(count):
                    site = random.choice(list(self.review_generator.gambling_sites.keys()))
                    example = self.review_generator.generate_comprehensive_review(site)
                    examples.append(example)
            
            elif example_type == "qa_pairs":
                for _ in range(count):
                    category = random.choice(self.qa_generator.question_categories)
                    example = self.qa_generator.generate_qa_pair(category)
                    examples.append(example)
            
            elif example_type == "seo_content":
                topics = ["best_gambling_sites", "gambling_bonuses"]
                for _ in range(count):
                    topic = random.choice(topics)
                    example = self.seo_generator.generate_seo_article(topic)
                    examples.append(example)
            
            elif example_type == "comparisons":
                sites = list(self.review_generator.gambling_sites.keys())
                for _ in range(count):
                    site1, site2 = random.sample(sites, 2)
                    example = self.review_generator.generate_comparison_review(site1, site2)
                    examples.append(example)
            
            elif example_type == "interactions":
                for _ in range(count):
                    example = self.interaction_simulator.generate_customer_support_conversation()
                    examples.append(example)
        
        # Validate examples
        validated_examples = []
        for example in examples:
            is_valid, issues = self.validator.validate_example(example)
            if is_valid:
                validated_examples.append(example)
            else:
                logger.warning(f"Rejected example {example.id}: {', '.join(issues)}")
        
        logger.info(f"Generated {len(validated_examples)} valid examples out of {len(examples)} total")
        return validated_examples
    
    def save_examples(self, examples: List[TrainingExample], filename: str = None):
        """Save examples to JSON file"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_data_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        # Convert to serializable format
        data = {
            "metadata": {
                "generated_at": datetime.datetime.now().isoformat(),
                "total_examples": len(examples),
                "generator_version": "1.0.0"
            },
            "examples": [asdict(example) for example in examples]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(examples)} examples to {filepath}")
        return filepath
    
    def generate_and_save(self, batch_size: int = 100, filename: str = None):
        """Generate a batch and save it immediately"""
        examples = self.generate_batch(batch_size)
        filepath = self.save_examples(examples, filename)
        return examples, filepath

def main():
    """Main function to run the data generator"""
    parser = argparse.ArgumentParser(description="Generate training data for LLM improvement")
    parser.add_argument("--batch-size", type=int, default=100, help="Number of examples to generate")
    parser.add_argument("--output-dir", type=str, default="training_data", help="Output directory")
    parser.add_argument("--filename", type=str, help="Output filename (optional)")
    parser.add_argument("--continuous", action="store_true", help="Run in continuous mode")
    parser.add_argument("--interval", type=int, default=3600, help="Interval in seconds for continuous mode")
    
    args = parser.parse_args()
    
    # Create data manager
    manager = TrainingDataManager(args.output_dir)
    
    if args.continuous:
        import time
        logger.info(f"Starting continuous generation mode with {args.interval}s intervals")
        
        while True:
            try:
                examples, filepath = manager.generate_and_save(args.batch_size)
                logger.info(f"Generated batch of {len(examples)} examples")
                time.sleep(args.interval)
            except KeyboardInterrupt:
                logger.info("Stopping continuous generation")
                break
            except Exception as e:
                logger.error(f"Error in continuous generation: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    else:
        # Single batch generation
        examples, filepath = manager.generate_and_save(args.batch_size, args.filename)
        print(f"Generated {len(examples)} training examples")
        print(f"Saved to: {filepath}")
        
        # Print statistics
        type_counts = {}
        for example in examples:
            type_counts[example.type] = type_counts.get(example.type, 0) + 1
        
        print("\nExample type distribution:")
        for example_type, count in type_counts.items():
            print(f"  {example_type}: {count}")

if __name__ == "__main__":
    main()