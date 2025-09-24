import requests
from datetime import datetime
from typing import Optional, List, Dict, Any
from urllib.parse import urlencode


class BoardsApiClient:
    def __init__(self, base_url: str = "http://localhost:8080", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def search_boards(
        self,
        nickname: Optional[str] = None,
        board_type: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100
    ) -> bytes:
        """Search boards using the same parameters as ParseSearchBoardParams"""
        params = {}
        
        if nickname:
            params["nickname"] = nickname
        if board_type:
            params["boardType"] = board_type
        if created_from:
            params["createdFrom"] = created_from.isoformat()
        if created_to:
            params["createdTo"] = created_to.isoformat()
        
        params["page"] = page
        params["pageSize"] = page_size
        
        url = f"{self.base_url}/boards"
        if params:
            url += f"?{urlencode(params)}"
        
        response = self.session.get(url)
        response.raise_for_status()
        return response.content

    def download_all_boards(
        self,
        nickname: str,
        output_dir: str = ".",
        board_type: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        page_size: int = 100
    ) -> int:
        """Download all boards for a user in chunks"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        page = 1
        total_files = 0
        
        while True:
            try:
                content = self.search_boards(
                    nickname=nickname,
                    board_type=board_type,
                    created_from=created_from,
                    created_to=created_to,
                    page=page,
                    page_size=page_size
                )
                
                if not content or content.strip() == b"% PBN 2.1":
                    break
                    
                filename = f"{nickname}_boards_page_{page}.pbn"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                total_files += 1
                page += 1
                
            except Exception:
                break
                
        return total_files
