from PilotClasses import Pilot
from pathlib import Path

def getHeaderDetailedRanking():
    # Basic HTML structure with the head section
    tab_htmlbody = '<!DOCTYPE html><html>'
    tab_htmlbody += '<head><title>Ranking MyRCM</title>'
    tab_htmlbody += '<meta charset="UTF-8">'
    
    # Add the AJAX script to fetch both the header and table content dynamically
    tab_htmlbody += """
    <script>
        function updateTable() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/updateTable', true);  // Request the table content from the server

            xhr.onload = function() {
                if (xhr.status == 200) {
                    // Parse the response (assuming it's a JSON with both thead and tbody)
                    var data = JSON.parse(xhr.responseText);
                    
                    // Update the thead and tbody with new content
                    document.querySelector('thead').innerHTML = data.thead;
                    document.querySelector('tbody').innerHTML = data.tbody;
                }
            };
            xhr.send();
        }
        // Automatically refresh the table and header every 10 seconds
        setInterval(updateTable, 500);
    </script>
    """
    
    # Link to the CSS file for styling
    tab_htmlbody += '<link href="detailedRankingStyle.css" rel="stylesheet">'
    tab_htmlbody += '</head>'

    # Body tag with background and centered table style
    tab_entete = '''
    <body style="background-image: url('BackGround.jpg'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center;">
        <table>
            <colgroup>
                <col style="width:40px" />
                <col style="width:40px" />
                <col style="width:500px" />
                <col style="width:70px" />
                <col style="width:90px" />
                <col style="width:90px" />
                <col style="width:90px" />
                <col style="width:150px" />
                <col style="width:50px" />
            </colgroup>
            <thead>
                <!-- The header will be dynamically loaded here using AJAX -->
                <tr><td>Loading...</td></tr>
            </thead>
            <tbody>
                <!-- The table body will be dynamically loaded here using AJAX -->
                <tr><td>Loading...</td></tr>
            </tbody>
        </table>
    </body>
    </html>
    '''
    
    # Concatenate the body part with the header and return it
    tab_htmlbody += tab_entete
    return tab_htmlbody


def getPilotDetailedRanking(pilot, showPilotCountryFlag=False):
    style = 'style="color: lightgreen;"' if pilot.newPosition else ''
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

def generateTableHTML(Serie, RaceTime, pilots):
    # Create the <thead> with dynamic Serie and RaceTime
    thead = f'''
    <tr>
        <td colspan="9" style="height: 60px; font-size: 35px; color: royalblue font-family: Montserrat;">{Serie}<br>{RaceTime}</td>
    </tr>
    <tr>
        <th></th>
        <th>N°</th>
        <th>Pilote</th>
        <th>Tours</th>
        <th>Last</th>
        <th>Best</th>
        <th>Med</th>
        <th>Prevision</th>
        <th>\u2195</th>
    </tr>
    '''

    # Create the <tbody> by iterating over pilots
    tbody = "<tbody>"
    for pilot in pilots:
        tbody += getPilotDetailedRanking(pilot, showPilotCountryFlag=False)
    tbody += "</tbody>"

    # Serve thead and tbody as a JSON response
    return {"thead": thead, "tbody": tbody}




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
    style = 'style="color: lightgreen;"' if pilot.newPosition else ''
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