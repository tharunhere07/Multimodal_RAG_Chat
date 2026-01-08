"""
YouTube video processor for extracting transcripts
"""
from typing import List, Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import yt_dlp
import re
from llama_index.core import Document


class YouTubeProcessor:
    """Handles processing of YouTube videos"""
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID or None
        """
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def get_video_info(url: str) -> dict:
        """
        Get video metadata using yt-dlp
        
        Args:
            url: YouTube URL
            
        Returns:
            Dictionary with video information
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'author': info.get('uploader', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date', ''),
                    'view_count': info.get('view_count', 0)
                }
        except Exception as e:
            return {
                'title': 'Unknown',
                'author': 'Unknown',
                'duration': 0,
                'description': '',
                'error': str(e)
            }
    
    @staticmethod
    def get_transcript(video_id: str, languages: List[str] = ['en']) -> Optional[str]:
        """
        Get transcript for a YouTube video
        
        Args:
            video_id: YouTube video ID
            languages: List of preferred languages
            
        Returns:
            Transcript text or None
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript_text = ' '.join([item['text'] for item in transcript_list])
            return transcript_text
        except (TranscriptsDisabled, NoTranscriptFound):
            # Try to get auto-generated captions
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_generated_transcript(languages)
                transcript_data = transcript.fetch()
                transcript_text = ' '.join([item['text'] for item in transcript_data])
                return transcript_text
            except Exception:
                return None
        except Exception:
            return None
    
    @classmethod
    def process_youtube_url(cls, url: str) -> List[Document]:
        """
        Process a YouTube URL and return LlamaIndex Documents
        
        Args:
            url: YouTube URL
            
        Returns:
            List of LlamaIndex Document objects
        """
        video_id = cls.extract_video_id(url)
        
        if not video_id:
            return [Document(
                text="Invalid YouTube URL provided.",
                metadata={'error': 'Invalid URL', 'source': 'youtube'}
            )]
        
        # Get video info
        video_info = cls.get_video_info(url)
        
        # Get transcript
        transcript = cls.get_transcript(video_id)
        
        if not transcript:
            text = f"Video Title: {video_info['title']}\n"
            text += f"Author: {video_info['author']}\n"
            text += f"Description: {video_info['description']}\n"
            text += "\n[Note: Transcript not available for this video]"
        else:
            text = f"Video Title: {video_info['title']}\n"
            text += f"Author: {video_info['author']}\n"
            text += f"Description: {video_info['description']}\n\n"
            text += f"Transcript:\n{transcript}"
        
        return [Document(
            text=text,
            metadata={
                'source': 'youtube',
                'video_id': video_id,
                'url': url,
                'title': video_info['title'],
                'author': video_info['author'],
                'duration': video_info['duration'],
                'has_transcript': transcript is not None
            }
        )]
