from PilotClasses import Pilot
from pathlib import Path

def getHeaderDetailedRanking(RaceTime="", Serie=""):
    tab_htmlbody = '<!DOCTYPE html><html>'
    tab_htmlbody += f'<head><title>Ranking MyRCM - {Serie}</title>'
    tab_htmlbody += '<meta charset="UTF-8">'
    tab_htmlbody += "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    tab_htmlbody += '<link href="detailedRankingStyle.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    # Add body tag with background and centered table style
    tab_entete = f'<body style="background-image: url(\'BackGround.jpg\'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;">'
    tab_entete += f'<table><thead><tr><td colspan="9" style="height: 60px;font-size: 35px;font-family: Montserrat;">{Serie}<br>{RaceTime}</td></tr></thead>'

    # Table headers
    tab_entete += '<thead><tr><th></th>\
        <th>N°</th>\
        <th>Pilote</th>\
        <th>Tours</th>\
        <th>Last</th>\
        <th>Best</th>\
        <th>Med</th>\
        <th>Prevision</th>\
        <th>Tendance</th>\
        </tr></thead><tbody>'

    tab_htmlbody += tab_entete
    return tab_htmlbody

def getPilotDetailedRanking(pilot, showPilotCountryFlag=False):
    style = 'style="color: red;"' if pilot.newPosition else ''
    lapTimeStyle = 'style="color: gold;"' if pilot.newBest else style
    NumberStyle = f'style="color: #fff;text-shadow:\
            1px 1px 0 #000,\
            -1px 1px 0 #000,\
            -1px -1px 0 #000,\
            1px -1px 0 #000;\
        background-size: 100% 100%;\
        background-image: url(Ressources/{pilot.countryicon});"' if showPilotCountryFlag else style
    
    # POS / CAR / PILOT / NLAPS / Last / Best / Med / Forecast / Trend  
    return f"<tr>\
        <td {style}>{pilot.position+1}</td>\
        <td {NumberStyle}>{pilot.vehicle}</td>\
        <td {style}>{pilot.pilot.upper()}</td>\
        <td {style}>{pilot.laps}</td>\
        <td {lapTimeStyle}>{pilot.laptime_s:0.3f}</td>\
        <td {style}>{pilot.besttime_s:0.3f}</td>\
        <td {style}>{pilot.mediumtime_s:0.2f}</td>\
        <td {style}>{pilot.forecast_short}</td>\
        <td {style}>{pilot.trend}</td>\
        </tr>"



def getHeaderRanking(RaceTime="", showBestLap=False):
    tab_htmlbody = '<!DOCTYPE html><html>'
    # tab_htmlbody += '<head><title>Page Title</title><meta http-equiv="refresh" content="1">'
    tab_htmlbody += '<head>'
    tab_htmlbody += '<meta charset="UTF-8">'
    tab_htmlbody +=  "<script>function autoRefresh() {window.location = window.location.href;}setInterval('autoRefresh()', 300);</script>"
    tab_htmlbody += '<link href="style.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    tab_entete = '<body><table><thead><tr><td colspan="5" style="height: 60px;font-size: 35px;font-family: Montserrat;">'+RaceTime+'</td></tr></body></table></thead>'
    
    tab_entete += '<body><table><thead>'
    #POS / CAR / TEAM ( Logo + LibTeam ) / NbTour / PrevTrs / Best / Med / Rythme 5' / Rythme 1h  
    tab_entete += f"<tr><th>Pos</th>\
        <th>N°</th>\
        <th>Equipe</th>\
        <th>Tours</th>\
        <th>Last</th>\
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
        <td {style}>{pilot.laps}</td>\
        <td {lapTimeStyle}>{pilot.besttime_s if showBestLap else pilot.laptime_s:0.3f}</td>'
    if extended:
        output+= f'<td {style}>{pilot.besttime_s:0.3f}</td>\
        <td {style}>{pilot.delaytimeprevious}</td>\
        <td {style}>{pilot.forecast}</td>'

    return output+'</tr>'