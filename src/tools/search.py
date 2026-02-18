"""
Search Tools using DuckDuckGo
"""
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
import time


class TechSearchTool:
    """
    DuckDuckGo search wrapper optimized for technology research.
    """
    
    def __init__(self, max_results: int = 5, delay: float = 1.0):
        """
        Initialize search tool.
        
        Args:
            max_results: Maximum results per search query
            delay: Delay between searches to avoid rate limiting (seconds)
        """
        self.max_results = max_results
        self.delay = delay
    
    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform a single search query.
        
        Args:
            query: Search query string
            max_results: Override default max_results
            
        Returns:
            List of search results with title, body, and href
        """
        max_results = max_results or self.max_results
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    max_results=max_results,
                    region='wt-wt',  # Worldwide search
                    safesearch='off',
                ))
                
                # Format results
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        'title': result.get('title', ''),
                        'body': result.get('body', ''),
                        'href': result.get('href', ''),
                    })
                
                return formatted_results
        
        except Exception as e:
            print(f"Search failed for query '{query}': {str(e)}")
            return []
    
    def search_multiple(
        self,
        queries: List[str],
        max_results_per_query: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Perform multiple search queries with delay between them.
        
        Args:
            queries: List of search query strings
            max_results_per_query: Maximum results per query
            
        Returns:
            Combined list of all search results
        """
        all_results = []
        
        for i, query in enumerate(queries):
            results = self.search(query, max_results_per_query)
            all_results.extend(results)
            
            # Add delay between searches (except for the last one)
            if i < len(queries) - 1 and self.delay > 0:
                time.sleep(self.delay)
        
        return all_results
    
    def search_tech_stack(
        self,
        framework_names: List[str],
        search_aspects: Optional[List[str]] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for technology information with multiple aspects.
        
        Args:
            framework_names: List of framework/library names
            search_aspects: Aspects to search for (e.g., "pros cons", "comparison")
            
        Returns:
            Dictionary mapping framework names to their search results
        """
        if search_aspects is None:
            search_aspects = [
                "pros cons",
                "best practices 2026",
                "comparison",
            ]
        
        results_by_framework = {}
        
        for framework in framework_names:
            framework_results = []
            
            for aspect in search_aspects:
                query = f"{framework} {aspect}"
                results = self.search(query, max_results=3)
                framework_results.extend(results)
                
                # Small delay between aspect searches
                if self.delay > 0:
                    time.sleep(self.delay)
            
            results_by_framework[framework] = framework_results
        
        return results_by_framework
    
    def search_with_filters(
        self,
        query: str,
        include_keywords: Optional[List[str]] = None,
        exclude_keywords: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search with keyword filtering.
        
        Args:
            query: Base search query
            include_keywords: Results must contain at least one of these keywords
            exclude_keywords: Results must not contain these keywords
            
        Returns:
            Filtered search results
        """
        results = self.search(query)
        
        if not results:
            return []
        
        filtered_results = []
        
        for result in results:
            # Check combined text (title + body)
            text = (result.get('title', '') + ' ' + result.get('body', '')).lower()
            
            # Apply inclusion filter
            if include_keywords:
                if not any(keyword.lower() in text for keyword in include_keywords):
                    continue
            
            # Apply exclusion filter
            if exclude_keywords:
                if any(keyword.lower() in text for keyword in exclude_keywords):
                    continue
            
            filtered_results.append(result)
        
        return filtered_results
    
    def prioritize_official_sources(
        self,
        results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Prioritize official documentation and reputable tech sites.
        
        Args:
            results: Search results to prioritize
            
        Returns:
            Sorted search results with official sources first
        """
        official_domains = [
            'github.com',
            'npmjs.com',
            'reactjs.org',
            'vuejs.org',
            'angular.io',
            'svelte.dev',
            'nextjs.org',
            'dev.to',
            'medium.com',
            'stackoverflow.com',
            'mdn.mozilla.org',
        ]
        
        def priority_score(result: Dict[str, Any]) -> int:
            href = result.get('href', '').lower()
            
            # Official sources get highest priority
            for domain in official_domains:
                if domain in href:
                    return 10
            
            # Default priority
            return 0
        
        # Sort by priority (descending)
        return sorted(results, key=priority_score, reverse=True)


# Global search tool instance
_global_search_tool: Optional[TechSearchTool] = None


def get_search_tool() -> TechSearchTool:
    """
    Get or create a global TechSearchTool instance.
    
    Returns:
        Shared TechSearchTool instance
    """
    global _global_search_tool
    if _global_search_tool is None:
        _global_search_tool = TechSearchTool()
    return _global_search_tool
