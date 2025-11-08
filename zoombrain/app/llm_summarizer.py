# LLM-based summarization using free/open-source models

from typing import List, Dict, Optional
import os


class LLMSummarizer:
    """Generate meeting summaries using LLM"""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize LLM summarizer
        
        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        # For free/open-source alternatives, consider:
        # - Hugging Face Inference API (free tier)
        # - Ollama (local models)
        # - Together AI (free tier)
    
    def summarize_transcript(
        self,
        transcript_text: str,
        summary_style: str = "bullet_points",
        detail_level: str = "medium"
    ) -> str:
        """
        Generate summary from transcript
        
        Args:
            transcript_text: Full transcript text
            summary_style: Style of summary (bullet_points, narrative, executive)
            detail_level: Level of detail (brief, medium, detailed)
            
        Returns:
            Generated summary
        """
        # Try OpenAI first if API key is available
        if self.api_key:
            return self._summarize_with_openai(transcript_text, summary_style, detail_level)
        else:
            # Fallback to simple extractive summarization
            return self._extractive_summary(transcript_text, detail_level)
    
    def _summarize_with_openai(
        self,
        transcript_text: str,
        summary_style: str,
        detail_level: str
    ) -> str:
        """Use OpenAI API for summarization"""
        try:
            import openai
            openai.api_key = self.api_key
            
            style_prompts = {
                "bullet_points": "Create a bullet-point summary of the key points.",
                "narrative": "Write a narrative summary in paragraph form.",
                "executive": "Create an executive summary highlighting decisions and action items."
            }
            
            detail_prompts = {
                "brief": "Keep it concise, under 5 sentences.",
                "medium": "Provide a moderate level of detail.",
                "detailed": "Include comprehensive details and context."
            }
            
            prompt = f"""
            Summarize the following meeting transcript.
            {style_prompts.get(summary_style, style_prompts['bullet_points'])}
            {detail_prompts.get(detail_level, detail_prompts['medium'])}
            
            Transcript:
            {transcript_text[:4000]}  # Limit context length
            """
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return self._extractive_summary(transcript_text, detail_level)
    
    def _extractive_summary(self, text: str, detail_level: str) -> str:
        """
        Simple extractive summarization (fallback)
        Extracts most important sentences
        """
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Determine number of sentences to extract based on detail level
        num_sentences = {
            "brief": min(3, len(sentences)),
            "medium": min(5, len(sentences)),
            "detailed": min(10, len(sentences))
        }.get(detail_level, 5)
        
        # Simple scoring: longer sentences with more content words are more important
        scored_sentences = []
        for sentence in sentences:
            words = sentence.split()
            # Score based on length and presence of important keywords
            score = len(words)
            important_words = ['action', 'decision', 'agree', 'will', 'should', 'must', 'important']
            score += sum(3 for word in words if word.lower() in important_words)
            scored_sentences.append((score, sentence))
        
        # Sort by score and take top N
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        top_sentences = [sent for _, sent in scored_sentences[:num_sentences]]
        
        return "• " + "\n• ".join(top_sentences)
    
    def generate_action_items_summary(self, action_items: List[Dict]) -> str:
        """
        Generate formatted summary of action items
        
        Args:
            action_items: List of action item dictionaries
            
        Returns:
            Formatted action items text
        """
        if not action_items:
            return "No specific action items were identified."
        
        summary = "Action Items:\n\n"
        for i, item in enumerate(action_items, 1):
            assigned = ", ".join(item.get('assigned_to', ['Unassigned']))
            summary += f"{i}. **{assigned}**: {item.get('extracted_action', item.get('text', ''))}\n"
        
        return summary
    
    def generate_participant_summary(self, participants: Dict[str, Dict]) -> str:
        """
        Generate summary of participant engagement
        
        Args:
            participants: Dictionary of participants with their data
            
        Returns:
            Formatted participant summary
        """
        if not participants:
            return "No participant data available."
        
        summary = "Participant Engagement:\n\n"
        
        # Sort by speaking count
        sorted_participants = sorted(
            participants.items(),
            key=lambda x: x[1].get('speaking_count', 0),
            reverse=True
        )
        
        for name, data in sorted_participants:
            speaking_count = data.get('speaking_count', 0)
            total_words = data.get('total_words', 0)
            role = data.get('role', 'Participant')
            
            summary += f"• **{name}** ({role}): {speaking_count} contributions, {total_words} words\n"
        
        return summary
    
    def generate_sentiment_summary(self, sentiment_data: Dict[str, Dict]) -> str:
        """
        Generate summary of sentiment analysis
        
        Args:
            sentiment_data: Dictionary of participants with sentiment data
            
        Returns:
            Formatted sentiment summary
        """
        if not sentiment_data:
            return "No sentiment data available."
        
        summary = "Sentiment Analysis:\n\n"
        
        overall_sentiment = 0
        count = 0
        
        for name, data in sentiment_data.items():
            score = data.get('sentiment_score', 0)
            classification = data.get('classification', 'neutral')
            
            emoji = "😊" if classification == "positive" else "😐" if classification == "neutral" else "😟"
            summary += f"• **{name}**: {classification.title()} {emoji} (Score: {score:.1f})\n"
            
            overall_sentiment += score
            count += 1
        
        if count > 0:
            avg_sentiment = overall_sentiment / count
            summary += f"\n**Overall Meeting Sentiment**: {avg_sentiment:.1f}/100\n"
        
        return summary
