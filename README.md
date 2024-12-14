# GitHub Repository Description

## Torrent Management Automation Script

This Python script automates the management of torrents using the qBittorrent API, along with integration with Sonarr and Radarr for media management. The script performs the following key functions:

1. **Logging Configuration**: It sets up a logging mechanism to track activities and errors, storing logs in an `output.log` file.

2. **API Configuration**: The script configures the necessary API endpoints and authentication keys for both Sonarr and Radarr, as well as for the qBittorrent client.

3. **Client Authentication**: It establishes a connection to the qBittorrent client and handles authentication, ensuring that the client is logged in before performing any operations.

4. **Torrent Management**:
   - The script checks all torrents in the qBittorrent client and identifies inactive torrents that have not been active for over 7 days, excluding those tagged with "donotdelete". Inactive torrents that are either seeding or queued are deleted.
   - It also identifies torrents that have been downloading too slowly or are stuck in metadata download for over 3 days. These torrents are deleted as well.

5. **Integration with Radarr and Sonarr**:
   - For torrents categorized under Radarr (movies), the script looks up the corresponding movie in Radarr, retrieves its history, and marks the slow torrent as failed, prompting an automatic search for a better torrent.
   - For torrents categorized under Sonarr (TV shows), it performs a similar operation by looking up the series, retrieving its history, and marking the slow torrent as failed.

6. **Logging Information**: Throughout the process, the script logs relevant information about the torrents being processed, including their state, category, and last activity timestamp.

7. **Graceful Logout**: Finally, the script ensures that the qBittorrent client logs out after completing the operations.

This script is designed to streamline the management of torrents, ensuring that only active and efficient downloads are maintained, while also integrating seamlessly with media management tools like Sonarr and Radarr.

### Requirements
- Python 3.x
- `qbittorrent-api` library
- `pycliarr` library
- Access to a running instance of qBittorrent, Sonarr, and Radarr

### Usage
To use this script, ensure that you have the required libraries installed and that you have configured the API keys and URLs correctly. Run the script in an environment where it can access the necessary services.

Feel free to contribute to this project or use it as a basis for your own torrent management automation needs!