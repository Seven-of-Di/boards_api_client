import click
from datetime import datetime
from .client import BoardsApiClient


@click.command()
@click.option("--base-url", default="http://localhost:8080", help="API base URL")
@click.option("--api-key", help="API key for authentication")
@click.option("--nickname", help="Filter by user nickname")
@click.option("--board-type", type=click.Choice(["ranked", "daily_tournament"]), help="Filter by board type")
@click.option("--created-from", help="Filter boards created from date (ISO format)")
@click.option("--created-to", help="Filter boards created to date (ISO format)")
@click.option("--page", default=1, help="Page number")
@click.option("--page-size", default=20, help="Page size")
@click.option("--output", "-o", help="Output file path")
def search_boards(base_url, api_key, nickname, board_type, created_from, created_to, page, page_size, output):
    """Search boards using IntoBridge API"""
    client = BoardsApiClient(base_url, api_key)
    
    created_from_dt = datetime.fromisoformat(created_from) if created_from else None
    created_to_dt = datetime.fromisoformat(created_to) if created_to else None
    
    try:
        file_content = client.search_boards(
            nickname=nickname,
            board_type=board_type,
            created_from=created_from_dt,
            created_to=created_to_dt,
            page=page,
            page_size=page_size
        )
        
        if output:
            with open(output, 'wb') as f:
                f.write(file_content)
            click.echo(f"File saved to: {output}")
        else:
            click.echo(file_content.decode('utf-8'))
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@click.command()
@click.option("--base-url", default="http://localhost:8080", help="API base URL")
@click.option("--api-key", help="API key for authentication")
@click.option("--nickname", required=True, help="User nickname")
@click.option("--output-dir", "-o", default=".", help="Output directory")
@click.option("--board-type", type=click.Choice(["ranked", "daily_tournament"]), help="Filter by board type")
@click.option("--created-from", help="Filter boards created from date (ISO format)")
@click.option("--created-to", help="Filter boards created to date (ISO format)")
@click.option("--page-size", default=20, help="Page size")
def download_all_boards(base_url, api_key, nickname, output_dir, board_type, created_from, created_to, page_size):
    """Download all boards for a user in chunks"""
    client = BoardsApiClient(base_url, api_key)
    
    created_from_dt = datetime.fromisoformat(created_from) if created_from else None
    created_to_dt = datetime.fromisoformat(created_to) if created_to else None
    
    try:
        total_files = client.download_all_boards(
            nickname=nickname,
            output_dir=output_dir,
            board_type=board_type,
            created_from=created_from_dt,
            created_to=created_to_dt,
            page_size=page_size
        )
        
        click.echo(f"Downloaded {total_files} files to {output_dir}")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)


@click.group()
def main():
    """Boards API Client"""
    pass


main.add_command(search_boards)
main.add_command(download_all_boards)