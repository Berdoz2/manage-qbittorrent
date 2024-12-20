import qbittorrentapi
import datetime
from pycliarr.api import SonarrCli, RadarrCli
import requests
import json
import logging

##
## Config Logger
##
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='output.log', encoding='utf-8', level=logging.INFO)

##
## Config Sonarr & Radarr
##
baseUrlSonarr = "http://192.168.1.140:8989"
apikeySonarr = "YOUR_API_KEY"
baseUrlRadarr = "http://192.168.1.140:7878"
apikeyRadarr = "YOUR_API_KEY"

sonarr = SonarrCli(baseUrlSonarr, apikeySonarr)
radarr = RadarrCli(baseUrlRadarr, apikeyRadarr)

##
## Config Qbittorrent
##
qbtHost = "192.168.1.140"
qbtPort = 8080
qbtUsername = "YOUR_USERNAME"
qbtPassword = "YOUR_PASSWORD"

# instantiate a Client using the appropriate WebUI configuration
conn_info = dict(
    host=qbtHost,
    port=qbtPort,
    username=qbtUsername,
    password=qbtPassword,
)
qbt_client = qbittorrentapi.Client(**conn_info)

# the Client will automatically acquire/maintain a logged-in state
# in line with any request. therefore, this is not strictly necessary;
# however, you may want to test the provided login credentials.
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    logger.error(e)


#Check all torrent
for torrent in qbt_client.torrents_info():
    #+7 days last activity + don't have tag "donotdelete" + is not downloading or meta downloading right now.
    #torrent to delete that is inactive
    if (datetime.datetime.fromtimestamp(torrent.last_activity) < datetime.datetime.today() - datetime.timedelta(days=7)) \
    and (torrent.tags != "donotdelete" and (torrent.state == "stalledUP" or torrent.state == "queuedUP")):
        logger.info(f"inactif | {torrent.name} ({torrent.state})")
        #delete this torrent
        qbt_client.torrents_delete(True, torrent.hash)

    #delete torrent that is not downloading fast enought or lock in Dl metadata
    elif (datetime.datetime.fromtimestamp(torrent.added_on)) > datetime.datetime.now() - datetime.timedelta(days=3) \
    and torrent.tags != "donotdelete" and (torrent.state == "downloading" or torrent.state == "metaDL" or torrent.state == "stalled"):
        logger.info(f"download too slow | {torrent.name} ({torrent.state})")
        #delete this torrent
        qbt_client.torrents_delete(True, torrent.hash)

        #Radarr
        if(torrent.category == "radarr"):
            responseRadarrMovies = radarr.lookup_movie(torrent.name)
            #Exctract id
            idFilm = str(responseRadarrMovies[0].id)

            #Get history of this film sorted by newest
            UrlHistory = baseUrlRadarr + "/api/v3/history/movie?movieId=" + idFilm + "&includeMovie=false&apikey=" + apikeyRadarr
            #Exctract id torrent 
            responseRadarrHistory = requests.get(UrlHistory)
            infoFilm = json.loads(responseRadarrHistory.text)
            idTorrentHistoryFilm = str(infoFilm[0]['id'])

            #Then get ID of the newest record
            #Ban slow torrent, automatic search after this torrent is ban
            URL = baseUrlRadarr + "/api/v3/history/failed/" + idTorrentHistoryFilm + "?apikey=" + apikeyRadarr
            responseMarkedAsFailedFilm = requests.post(URL)
            logger.info("Respond command marked as failed film : " + responseMarkedAsFailedFilm)

        #Sonarr
        elif(torrent.category == "tv-sonarr"):
            responseSonarrSeries = sonarr.lookup_serie(torrent.name)
            #Exctract id
            idSerie = str(responseSonarrSeries[0].id)

            #Get history of this film sorted by newest
            UrlHistory = baseUrlSonarr + "/api/v3/history/series?movieId=" + idSerie + "&includeMovie=false&apikey=" + apikeySonarr
            #Exctract id torrent
            responseSonarrHistory = requests.get(UrlHistory)
            infoSerie = json.loads(responseSonarrHistory.text)
            idTorrentHistorySerie = str(infoSerie[0]['id'])

            #Then get ID of the newest record
            #Ban slow torrent, automatic search after this torrent is ban
            URL = baseUrlSonarr + "/api/v3/history/failed/" + idTorrentHistorySerie + "?apikey=" + apikeySonarr
            responseMarkedAsFailedSerie = requests.post(URL)
            logger.info("Respond command marked as failed serie : " + responseMarkedAsFailedSerie)
        else:
            logger.info("This torrent is not a film or serie : " + torrent.name)

    else :
        # retrieve and show all torrents
        logger.info(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state}) ({torrent.category}) ({torrent.tags}) ({datetime.datetime.fromtimestamp(torrent.last_activity)})")
    

# if the Client will not be long-lived or many Clients may be created
# in a relatively short amount of time, be sure to log out:
qbt_client.auth_log_out()