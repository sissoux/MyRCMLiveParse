from PilotClasses import Pilot
from pathlib import Path

def getHeaderStatTable(RaceTime=""):
    tab_htmlbody = '<!DOCTYPE html><html>'
    tab_htmlbody += '<head><title>Page Title</title>'
    tab_htmlbody += '<meta http-equiv="refresh" content="1">'
    tab_htmlbody += '<head>'
    tab_htmlbody += '<meta charset="UTF-8">'
    # htmlbody +=  "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    tab_htmlbody += '<link href="tableau.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    tab_entete = '<body><table><thead>'
    tab_entete += '<tr><td colspan="11" id="timming" style="height: 60px;font-size: 50px;font-family: Montserrat;">'+RaceTime+'</td></tr>'
    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    tab_entete += f"<tr><th>Pos</th>\
        <th>N°</th>\
        <th></th>\
        <th>Equipe</th>\
        <th>Tours</th>\
        <th>Previsionel</th>\
        <th>Best</th>\
        <th>Med</th>\
        <th>Tendance</th>\
        <th>Rythme 5min</th>\
        <th>Rythme 1h</th>\
        </tr>"
    tab_entete += '</thead><tbody>'
    tab_htmlbody += tab_entete

    return tab_htmlbody




def getPilotStatTable(pilot:Pilot, baseLogoPath:Path):

    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    return f"<tr>\
        <td>{pilot.position+1}</td>\
        <td>{pilot.vehicle}</td>\
        <td><img class='logo' src='{baseLogoPath}\\{pilot.vehicle}.png'/></td>\
        <td>{pilot.TeamName.upper()}</td>\
        <td>{pilot.laps}</td>\
        <td>{pilot.forecast_short}</td>\
        <td>{pilot.besttime_s:0.3f}</td>\
        <td>{pilot.mediumtime_s}</td>\
        <td>{pilot.trend}</td>\
        <td>{pilot.pace_5m}</td>\
        <td>{pilot.pace_1h}</td>\
        </tr>"


def getHeaderRanking(RaceTime="", showBestLap=False, extended=False):
    tab_htmlbody = '<!DOCTYPE html><html>'
    tab_htmlbody += '<head><title>Page Title</title><meta http-equiv="refresh" content="2">'
    tab_htmlbody += '<head>'
    tab_htmlbody += '<meta charset="UTF-8">'
    # tab_htmlbody +=  "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    tab_htmlbody += '<link href="style.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    tab_entete = '<body><table><thead><tr><td colspan="8" style="height: 60px;font-size: 35px;font-family: Montserrat;">'+RaceTime+'</td></tr></body></table></thead>'
    
    tab_entete += '<body><table><thead>'
    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    tab_entete += f"<tr><th></th>\
        <th>N°</th>\
        <th>Pilote</th>\
        <th>Tours</th>\
        <th>Last</th>\
        <th>Best</th>\
        <th>Ecart</th>\
        <th>Prevision</th>\
        </tr>"
    tab_entete += '</thead><tbody>'
    tab_htmlbody += tab_entete

    return tab_htmlbody

def getPilotRanking(pilot:Pilot, showBestLap=False, showPilotCountryFlag=False, extended=False):
    style = 'style="color: red;"' if pilot.newPosition else ''
    lapTimeStyle = 'style="color: gold;"' if pilot.newBest else style
    NumberStyle = f'style="color: #fff;text-shadow:\
            1px 1px 0 #000,\
            -1px 1px 0 #000,\
            -1px -1px 0 #000,\
            1px -1px 0 #000;\
        background-size: 100% 100%;\
        background-image: url(Ressources/{pilot.countryicon});"' if showPilotCountryFlag else style

    output = f'<tr>\
        <td {style}>{pilot.position+1}</td>\
        <td {NumberStyle}>{pilot.vehicle}</td>\
        <td {style}>{pilot.pilot.upper()}</td>\
        <td {style}>{pilot.laps}</td>'
    if extended:
        output+=f'<td {style}>{pilot.laptime_s:0.3f}</td>\
        <td {style}>{pilot.besttime_s:0.3f}</td>\
        <td {style}>{pilot.delaytimeprevious}</td>\
        <td {style}>{pilot.forecast}</td>'

    return output+'</tr>'