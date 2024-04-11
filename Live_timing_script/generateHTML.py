from PilotClasses import Pilot
from pathlib import Path

def getHeaderTable(RaceTime=""):
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



def getHeader(RaceTime=""):
    tab_htmlbody = '<!DOCTYPE html><html>'
    tab_htmlbody += '<head><title>Page Title</title><meta http-equiv="refresh" content="1">'
    tab_htmlbody += '<head>'
    tab_htmlbody += '<meta charset="UTF-8">'
    # htmlbody +=  "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    tab_htmlbody += '<link href="tableau.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    tab_entete = '<body><table><thead>'
    tab_entete += '<tr><td colspan="10" id="timming" style="height: 60px;font-size: 50px;font-family: Montserrat;">'+RaceTime+'</td></tr>'
    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    tab_entete += f"<tr><th>Pos</th>\
        <th>N°</th>\
        <th></th>\
        <th>Equipe</th>\
        <th>Tours</th>\
        <th>Previsionel</th>\
        <th>Best</th>\
        <th>Med</th>\
        <th>Ryt 5min</th>\
        <th>Ryt 1h</th>\
        </tr>"
    tab_entete += '</thead><tbody>'
    tab_htmlbody += tab_entete

    return tab_htmlbody

def getPilotTable(pilot:Pilot, baseLogoPath:Path):

    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    return f"<tr>\
        <td>{pilot.position+1}</td>\
        <td>{pilot.vehicle}</td>\
        <td><img class='logo' src='{baseLogoPath}\\{pilot.vehicle}.png'/></td>\
        <td>{pilot.pilot.upper()}</td>\
        <td>{pilot.laps}</td>\
        <td>{pilot.forecast.split()[0]}</td>\
        <td>{pilot.besttime_s:0.3f}</td>\
        <td>{pilot.mediumtime_s}</td>\
        <td>{pilot.trend}</td>\
        <td>{pilot.pace_5m}</td>\
        <td>{pilot.pace_1h}</td>\
        </tr>"


def getPilot(pilot:Pilot, baseLogoPath:Path):

    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    return f"<tr>\
        <td>{pilot.position+1}</td>\
        <td>{pilot.vehicle}</td>\
        <td><img class='logo' src='{baseLogoPath}\\{pilot.vehicle}.png'/></td>\
        <td>{pilot.pilot.upper()}</td>\
        <td>{pilot.laps}</td>\
        <td>{pilot.forecast}</td>\
        <td>{pilot.besttime_s:0.3f}</td>\
        <td>{pilot.mediumtime_s}</td>\
        <td>{pilot.pace_5m}</td>\
        <td>{pilot.pace_1h}</td>\
        </tr>"