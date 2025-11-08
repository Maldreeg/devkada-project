# Sentiment analysis for meeting transcripts

from typing import Dict, List, Tuple
import re


class SentimentAnalyzer:
    """Analyze sentiment in meeting transcripts"""
    
    def __init__(self):
        # Sentiment word lexicons (simplified - can be replaced with better models)
        self.positive_words = {
            'excellent', 'great', 'good', 'wonderful', 'fantastic', 'amazing',
            'awesome', 'brilliant', 'outstanding', 'superb', 'love', 'perfect',
            'agree', 'yes', 'definitely', 'absolutely', 'congratulations', 'success',
            'achievement', 'progress', 'improve', 'benefit', 'opportunity', 'excited',
            'happy', 'pleased', 'satisfied', 'grateful', 'thank', 'appreciate'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'disappointing',
            'unfortunate', 'problem', 'issue', 'concern', 'worried', 'anxious',
            'difficult', 'challenge', 'struggle', 'fail', 'failure', 'mistake',
            'error', 'wrong', 'disagree', 'no', 'never', 'cannot', 'impossible',
            'frustrated', 'angry', 'upset', 'unhappy', 'dissatisfied', 'delay'
        }
        
        self.intensifiers = {
            'very': 1.5, 'really': 1.5, 'extremely': 2.0, 'absolutely': 2.0,
            'completely': 2.0, 'totally': 2.0, 'highly': 1.5
        }
        
        self.negations = {'not', 'no', 'never', "n't", 'neither', 'nor', 'none'}
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment score and classification
        """
        words = text.lower().split()
        score = 0
        word_count = len(words)
        
        for i, word in enumerate(words):
            # Remove punctuation
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            # Check for negation in previous words
            negated = False
            if i > 0:
                prev_word = re.sub(r'[^\w\s]', '', words[i-1])
                if prev_word in self.negations:
                    negated = True
            
            # Check for intensifiers
            multiplier = 1.0
            if i > 0:
                prev_word = re.sub(r'[^\w\s]', '', words[i-1])
                multiplier = self.intensifiers.get(prev_word, 1.0)
            
            # Calculate sentiment
            if clean_word in self.positive_words:
                score += (1.0 * multiplier) * (-1 if negated else 1)
            elif clean_word in self.negative_words:
                score += (-1.0 * multiplier) * (-1 if negated else 1)
        
        # Normalize score to -100 to 100 range
        if word_count > 0:
            normalized_score = (score / word_count) * 100
            normalized_score = max(-100, min(100, normalized_score))
        else:
            normalized_score = 0
        
        # Classify sentiment
        if normalized_score >= 20:
            classification = "positive"
        elif normalized_score <= -20:
            classification = "negative"
        else:
            classification = "neutral"
        
        return {
            'score': normalized_score,
            'classification': classification,
            'raw_score': score,
            'word_count': word_count
        }
    
    def analyze_participant_sentiment(
        self, 
        segments: List[Dict], 
        participants: Dict[str, Dict]
    ) -> Dict[str, Dict]:
        """
        Analyze sentiment for each participant
        
        Args:
            segments: List of transcript segments
            participants: Dictionary of participants
            
        Returns:
            Dictionary of participants with their sentiment analysis
        """
        participant_sentiments = {}
        
        for participant_name in participants.keys():
            participant_texts = [
                seg['text'] for seg in segments 
                if seg.get('speaker') == participant_name
            ]
            
            if participant_texts:
                # Combine all text for this participant
                combined_text = ' '.join(participant_texts)
                sentiment = self.analyze_text(combined_text)
                
                participant_sentiments[participant_name] = {
                    'sentiment_score': sentiment['score'],
                    'classification': sentiment['classification'],
                    'total_statements': len(participant_texts),
                    'avg_words_per_statement': sentiment['word_count'] / len(participant_texts)
                }
            else:
                participant_sentiments[participant_name] = {
                    'sentiment_score': 0,
                    'classification': 'neutral',
                    'total_statements': 0,
                    'avg_words_per_statement': 0
                }
        
        return participant_sentiments
    
    def calculate_engagement_heatmap(
        self, 
        segments: List[Dict], 
        time_window_minutes: int = 5
    ) -> List[Dict]:
        """
        Calculate engagement levels over time
        
        Args:
            segments: List of transcript segments with timestamps
            time_window_minutes: Time window for aggregation
            
        Returns:
            List of time windows with engagement metrics
        """
        # This is a simplified version - would need actual timestamp parsing
        heatmap = []
        
        if not segments:
            return heatmap
        
        # Group segments into time windows
        window_size = time_window_minutes
        current_window = {
            'window': f'0-{window_size} min',
            'speaker_count': 0,
            'word_count': 0,
            'sentiment_score': 0,
            'speakers': set()
        }
        
        segment_count = 0
        for i, segment in enumerate(segments):
            current_window['word_count'] += len(segment['text'].split())
            current_window['speakers'].add(segment.get('speaker', 'Unknown'))
            sentiment = self.analyze_text(segment['text'])
            current_window['sentiment_score'] += sentiment['score']
            segment_count += 1
            
            # Create new window every N segments (approximation without real timestamps)
            if (i + 1) % 10 == 0 or i == len(segments) - 1:
                current_window['speaker_count'] = len(current_window['speakers'])
                current_window['avg_sentiment'] = (
                    current_window['sentiment_score'] / segment_count 
                    if segment_count > 0 else 0
                )
                current_window['speakers'] = list(current_window['speakers'])
                
                # Calculate engagement score (combination of activity and sentiment)
                engagement_score = (
                    (current_window['speaker_count'] * 10) +
                    (current_window['word_count'] / 10) +
                    (current_window['avg_sentiment'] / 2)
                )
                current_window['engagement_score'] = max(0, min(100, engagement_score))
                
                heatmap.append(current_window.copy())
                
                # Reset for next window
                window_start = len(heatmap) * window_size
                current_window = {
                    'window': f'{window_start}-{window_start + window_size} min',
                    'speaker_count': 0,
                    'word_count': 0,
                    'sentiment_score': 0,
                    'speakers': set()
                }
                segment_count = 0
        
        return heatmap
    
    def identify_sentiment_triggers(
        self, 
        segments: List[Dict]
    ) -> Dict[str, List[str]]:
        """
        Identify what topics or phrases trigger positive/negative sentiment
        
        Args:
            segments: List of transcript segments
            
        Returns:
            Dictionary of positive and negative triggers
        """
        triggers = {
            'positive': [],
            'negative': []
        }
        
        for segment in segments:
            sentiment = self.analyze_text(segment['text'])
            
            if sentiment['score'] > 50:
                triggers['positive'].append(segment['text'][:100])
            elif sentiment['score'] < -50:
                triggers['negative'].append(segment['text'][:100])
        
        return triggers
    
    def should_send_sentiment_notification(self, sentiment_score: float) -> Tuple[bool, str]:
        """
        Determine if a sentiment notification should be sent
        
        Args:
            sentiment_score: Sentiment score (-100 to 100)
            
        Returns:
            Tuple of (should_send, message_type)
        """
        if sentiment_score >= 80:
            return True, "positive"
        elif sentiment_score <= -80:
            return True, "negative"
        else:
            return False, "none"
