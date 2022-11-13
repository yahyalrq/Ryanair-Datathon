import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import datetime
import pydeck as pdk
from utils import load_model, get_distance, update_df
from utils import load_dataset

################################################################
# JAVASCRIPT
################################################################
#[theme]
#base="dark"
#primaryColor="#cebc03"
#secondaryBackgroundColor="#0035bd"

def render_forecast():
    single, csv = st.tabs(['Live Prediction', 'CSV Predictions'])
    with csv:
        ## TBD
        file_uploaded = st.file_uploader('Upload file with all necessary variables', type='CSV')

        # Currently disabled since it's not working
        st.download_button('Download predictions as CSV', data='csv', file_name='data/extended_insights.csv', disabled=True)

    with single:
        st.markdown(""" 
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel="stylesheet" href="../css/style.css">
            <link href='https://fonts.googleapis.com/css?family=Allerta Stencil' rel='stylesheet'>
        <style>
                h1{font-display: aligncenter;
                    font-family: 'Allerta Stencil';
                    color: white;}
        </style>
        <h1><center>Teledyne Ramp Weight Forecast</center></h1>
        </head>
        </html>
        """, unsafe_allow_html=True)

        st.write('') # adds space between title and form
        form = st.form(key="annotation")

        with form:
            df = []
            col = st.columns(3)
            Aircraft_registration = col[0].selectbox('Aircraft registration',
            #st.write('Aircraft registration is', Aircraft_registration)
            ('SPRZK', '9HQEC', '9HQCN', 'SPRKP', 'EIDWJ', '9HQBG', '9HQDH','EIEBR', 'SPRSD', 'EIDYL', 'EIEBC', 'EIEKZ', 'EIDPH', '9HQCV','EIGXI', 'EIDHE', 'EIFIM', 'EIFZK', 'EIEVE', '9HQBQ', 'EIDHA','EIEXD', 'SPRSG', 'EIENY', 'EIDHH', 'EIDPG', '9HQDP', 'EIDWT','EIFZM', 'EIFTI', 'EIDWI', '9HQAH', '9HLOW', '9HQCC', 'EIDYE','9HQCB', 'EIEME', 'EIEBP', 'EIDHT', 'EIDHY', 'EIGSG', 'EIDCN','EIEKG', 'EIFIL', '9HQBW', 'EIEBX', 'EIDWS', 'EIDWO', 'EIDYD','9HQDE', 'EIEBI', 'EIEXE', '9HQAQ', 'SPRSL', '9HQDT', '9HQEP','SPRZH', '9HLMP', 'SPRKV', '9HQEF', 'EIEKR', 'EIGJB', 'SPRSB','9HQDO', 'EIEGA', 'EIEFK', '9HQEK', 'EIDPW', '9HQBV', 'EIESV','EIDLC', 'EIEBF', '9HQAV', 'EIFTN', '9HQDX', 'EIEBO', 'EIGSI','9HQAL', '9HQAM', '9HLOM', 'EIDPM', 'EIDHG', '9HQEA', '9HQCJ','9HQDM', '9HQAZ', 'EIDHW', '9HQAS', 'EIEBN', 'EIDWL', '9HQCH','EIDCG', 'SPRKD', 'EIEXF', '9HQDG', 'EIDCR', '9HQCU', 'SPRKN','EIEFZ', 'EIEVJ', '9HQBY', 'SPRSO', 'EIDYN', 'EIEKO', 'EIDYR','EIDWP', 'SPRSQ', 'EIEBM', 'SPRSC', 'EIDWV', 'EIDPZ', 'SPRKH','9HVUD', 'EIEVV', 'EIEMM', 'SPRKU', '9HQBN', 'OEIHH', 'EIDCH','EIFTP', '9HQBR', 'EIDHF', '9HQEG', 'EIGJS', '9HQBJ', 'EIDCZ','EIDCO', 'EIDCK', '9HQAT', 'EIDHC', 'EIDWR', 'EIEVI', 'SPRKL','9HQAE', '9HQAI', 'EIDLI', 'EIDYW', 'SPRZI', 'EIDLY', 'EIEKF','9HLOY', 'EIEMA', 'SPRSI', 'EIGDD', 'EIEVN', 'SPRSP', '9HQAP','EIGJD', 'EIDPD', 'EIDCX', 'EIDPV', 'EIENT', 'SPRSS', 'EIEKC','EIEPC', '9HQAU', 'EIDLR', '9HQCQ', '9HQCW', 'EIFIN', '9HVUW','EIDAJ', 'EIDWA', 'EIDHB', 'EIEVL', '9HVUQ', 'EIDWE', 'EIDAO','GRUKA', 'SPRZC', 'EIGSH', '9HQDA', '9HQBB', 'OEIBJ', 'EIDPP','9HQDU', 'EIEVK', '9HQCO', 'EIENF', 'EIEMF', 'EIGXK', '9HQAB','EIDYP', 'EIEBE', 'SPRSZ', 'EIDCL', '9HLOZ', 'EIEKD', 'EIEML','9HQBE', '9HQCX', 'EIEVB', 'SPRSK', 'EIGDN', 'EIDAM', 'EIFRP','EIENO', 'EIENA', 'EIGSJ', 'SPRKI', 'EIFTA', 'EIEMC', 'EIEKL','9HQEI', 'EIDHP', 'EIEMI', '9HQBK', 'EIEFO', 'SPRKM', '9HQAO','9HQBI', 'SPRSH', '9HQEN', '9HQCR', '9HQBD', 'EIGDM', 'EIDPJ','SPRSF', 'EIEFJ', 'EIDYM', '9HLMT', '9HQAA', 'EIDWF', '9HQEE','9HVUU', 'EIDLF', 'EIEBZ', 'EIDHX', 'EIDYB', 'SPRSN', '9HQAF','9HQBZ', 'EIEFY', 'EIEKV', '9HQDI', '9HQCA', '9HQEM', '9HQCL','9HQCI', 'EIDHS', 'GRUKD', 'EIDYA', '9HQCF', 'EIDAF', 'EIDAH','9HQAW', 'EIEKJ', 'EIEMJ', '9HQCZ', 'SPRSU', 'EIENK', '9HQAK','EIEGD', 'EIENC', 'EIEBL', 'EIEFH', 'EIDPK', 'EIDYV', 'SPRST','EIDCI', '9HQDD', 'EIDWD', 'EIEBK', '9HQBX', 'EIDWH', 'EIEVM','EIDYF', 'EIEBV', '9HLOI', 'EIDHZ', 'EIFIO', 'EIDWB', 'EIGJN','EIENP', '9HQBA', '9HQCK', '9HQDV', 'EIDLB', 'EIDLD', 'EIENI','EIEVO', 'EIEBA', 'EIDYC', 'EIENV', 'EIEKI', '9HQBP', 'EIGXL','SPRKR', 'EIDYZ', '9HQAJ', 'GRUKG', '9HQAX', 'EIGJH', 'EIFTH','EIEKS', 'SPRKE', 'SPRZB', '9HQDL', 'EIEFG', 'EIDWZ', 'EIDLG','EIDCP', 'SPRKW', 'EIEKE', 'SPRKG', 'SPRSE', 'EIDCY', 'EIEMB','EIEVC', '9HQEO', 'EIEBS', '9HQCY', '9HLMI', '9HQAD', 'EIFIY','SPRKF', 'EIEBH', '9HQCM', '9HQAC', 'SPRKB', 'EIEVS', 'EIEMO','EIEMP', '9HQEL', 'EIENW', 'EIEKK', 'SPRZF', 'EIDHO', '9HQDW','EIDWK', 'EIDYY', 'EIDPB', 'EIDLX', '9HQEB', 'OELMI', 'EIFOZ','9HQAY', '9HVUK', 'EIENJ', 'EIDWM', 'EIDHN', 'EIEST', '9HLOU','9HQBS', 'GRUKH', 'EIEPD', 'EIEKX', 'EIDLH', 'EIDWY', 'EIEVA','EIDAN', 'EIEFE', 'EIDHD', '9HQED', 'EIEBD', 'SPRSW', '9HQDY','SPRSA', 'EIDPO', 'GRUKC', 'EIGXJ', 'EIFZN', 'EIFIP', 'EIFRW','EIFIW', '9HQBO', 'EIDLK', '9HQEJ', '9HQDK', 'EIHEZ', 'EIEFF','9HQCD', 'EIEVX', 'EIEKM', 'EIDHV', 'EIEVT', '9HQDJ', '9HVUP','EIESN', 'EIEFC', 'EIEPA', '9HQBC', 'EIEBY', 'EIFRR', 'EIDWC', 'EIFZJ', 'EIDPT', '9HVUV', 'EIEKH', 'EIDLV', 'EIFRJ', '9HQBM','EIFIR', '9HVUM', 'EIEMD', 'EIEVR', 'SPRKC', 'EIGJJ', 'EIEKP','9HQBU', 'EIDPF', 'EIDCM', '9HQAG', 'EIDLW', 'EIEMN', '9HQBH','EIDAG', 'EIDPY', '9HQAN', 'SPRSM', '9HQDR', 'EIEMH', 'EIEMR','EIDWW', 'SPRKT', 'EIFIC', 'SPRSR', 'EIEVG', '9HQBL', 'EIEKW','EIFTV', 'EIDAK', 'EIDPI', '9HQCG', 'SPRKQ', 'SPRSY', '9HLOP','EIFRL', 'SPRZG', 'EIGJT', '9HQDS', 'EIFRG', 'EIENM', '9HQDZ','EIEPF', '9HQDQ', 'EIDWX', 'OELOR', 'EIESP', '9HQCP', 'EIDLN','EIHET', 'EIFOK', 'EIFOL', 'EIENN', 'EIFRX', '9HQCT', 'EIDYX','EIFIT', 'EIHEN', '9HQDF', 'EIFOS', 'EIFOV', 'EIFTR', '9HQBT','EIHGR', 'OELMB', 'EIEVH', '9HLMC', 'EIEFD', 'EIDCF', 'GRUKB','EIENS', 'EIFOP', 'EIDAR', 'SPRKS', 'EIEBW', 'EIEFI', 'EIFZO','EIGDZ', '9HQCS', 'EIDPN', 'EIGDF', 'EIENX', 'EIEFX', '9HQBF','EIENG', 'EIFOF', 'EIFRB', 'EIFIG', 'EIDAP', 'EIFID', '9HVUA','EIEVF', 'EIFTW', 'EIEPB', 'EIHAT', 'EIEKN', 'EIEKT', 'SPRZD','EIFIA', 'EIGXN', 'SPRSV', '9HQDB', 'EIGSK', 'EIENL', 'EIEFN','EIEBG', 'EIENB', 'EIDCW', '9HIHH', 'EIFIF', 'EIFIH', '9HQCE','EIEVP', 'EIDAL', '9HVUC', 'EIFTK', 'EIESS', '9HLOO', 'EIDPC','EIGXH', '9HLON', '9HVUJ', 'EIDYO', 'OELOY', 'EIEKY', 'EIDAS','EIHGW', 'OELOS', 'EIENH', 'SPRZE', 'EIEGB', '9HVUH', 'EIDCJ','EIFRK', 'EIFTG', '9HVUE', 'SPRKK', 'EIDHR', 'EIDLJ', '9HLMG','9HQEH', 'EIGXM', 'EIFIS', 'EIDLE', 'EIDAI', 'EIGJA', '9HQDC','SPRSX', 'EIFRE', 'EIEGC', '9HIBJ', 'EIDPR', 'EIEKB', '9HLAJ','EIDLO', 'EIFTT', '9HQDN', 'EIFRS', '9HQAR', 'EIDWG', 'EIGDY','9HLOQ', '9HVUG', 'EIEMK', '9HIHL', 'EIENR', 'OELOB', '9HLOB','9HVUL', 'EIENE', 'EIFOG', 'EIGXG', 'EIGJP', 'SPRZA', 'EIHEY','SPRKA', 'EIDPL', 'EIFZL', '9HLMB', 'EIFRY', '9HLOR', '9HVUN','EIHAY', 'OELOI', 'EIFOT', 'EIHGX', 'EIFTY', 'EIFTL', 'SPRKO','EIGJG', 'EIGJK', 'EIFIE', '9HLAX', '9HVUS', 'OELOJ', 'EIFTD','9HVUR', 'EIEVW', 'EIGDI', '9HVUF', 'EIDAE', 'OEIHD', 'EIFTM','9HVUI', 'EIFIJ', 'EIHAX', 'EIFTZ', 'EIHGP', '9HVUB', 'OELON','EIFTO', 'EIFIV', 'EIEPH', 'EIFZH', '9HIHD', '9HLOS', 'EIFTE','EIGDE', 'OELOW', '9HLMJ', 'EIFRI', 'EIFTC', 'EIGJO', 'OELOZ','EIHEV', 'GRUKF', 'EIGDK', 'EIHGT', 'EIHGO', '9HLMH', '9HLOT','OELOA', 'OELOP', 'EIFTS', 'OELOU', 'EIFTJ', 'EIFRT', 'EIFOO','EIFRM', 'EIFRH', 'OELOT', 'EIHMS', 'EIHGG', 'EIFOY', 'EIHAW','EIFOR', '9HVUT', 'EIFIB', 'SPRZL', 'EIFRC', 'EIEVY', 'EIGDC','EIFOB', 'EIGDO', '9HLOA', 'EIFOE', 'EIDPX', '9HVUO', 'EIFIK','EIFEH', 'EIFOM', '9HVUX', 'EIDAD', 'EIGJF', 'EIEKA', 'EIHGZ','EIHGY', 'EIFOJ', 'EIGDH', 'OELMG', 'OELOO', 'EIGDG', 'OELOQ','OELOX', 'EIGJE', 'EISEV', 'EIFOA', 'EIFEG', 'EIFOW', 'OEIHL','EIGJI', 'OELMC', 'EIFRZ', 'EIFTB', 'GRUKE', 'EIGJM', 'EIFRO','OELOM', 'EIDAC', 'EIHEW', 'EIFRD', 'EIHES', 'EIHGN', 'OELMJ','EIFOC', 'EIFEI', 'SPRZO', 'EIFOH', 'EIEVZ', 'EIFRV', 'EIFIZ'))
            df.append(Aircraft_registration)
            AircraftCapacity = col[1].selectbox('Aircraft Capacity', (197, 189, 180, 148))
            df.append(AircraftCapacity)
            AircraftTypeGroup = col[2].selectbox('Aircraft Type Group', ('Max', 'NG', 'Airbus'))
            df.append(AircraftTypeGroup)

            col = st.columns(3)
            ServiceDescription = col[0].selectbox('Service Description', ('Scheduled Flight', 'Charter Flight','Charter Flight (Tour Operator)', 'Positioning Flight'))
            df.append(ServiceDescription)
            Carrier = col[1].selectbox('Carrier', ('FR', 'RR', 'RK', 'OE'))
            df.append(Carrier)
            AOCDescription = col[2].selectbox('AOCDescription', ('Ryanair Sun', 'Malta Air', 'Ryanair DAC', 'Lauda Motion Europe','Lauda Motion', 'Ryanair UK'))
            df.append(AOCDescription)

            col = st.columns(2)
            Departure_location = col[0].selectbox(' Departure location',
            ('EMA', 'TRN', 'STN', 'DTM', 'BHX', 'BGY', 'PMO', 'CRL', 'OPO','MAD', 'MRS', 'VNO', 'BZR', 'LIS', 'DUB', 'PMI', 'TSF', 'FCO','PFO', 'GDN', 'ALC', 'FAO', 'IBZ', 'ZAG', 'OTP', 'CPH', 'ATH','TLV', 'BCN', 'TPS', 'AGP', 'CIA', 'EIN', 'CTA', 'BDS', 'SKG','VIE', 'NCL', 'WMI', 'SXF', 'FRA', 'BES', 'ESU', 'BVA', 'TRS','MXP', 'PEG', 'BRI', 'ACE', 'SVQ', 'MLA', 'LGW', 'BLQ', 'HHN','CGN', 'CAG', 'LBA', 'BUD', 'PRG', 'ORK', 'RIX', 'TLL', 'POZ','SUF', 'TLS', 'ZTH', 'LWO', 'VRN', 'NRN', 'KTW', 'AHO', 'GRO','KRK', 'BER', 'VLC', 'BOD', 'CFU', 'KBP', 'EDI', 'TRF', 'PSA','VCE', 'SCQ', 'WRO', 'PDL', 'BRU', 'BRS', 'NDR', 'BTS', 'FMM','LPL', 'MAN', 'RBA', 'SDR', 'SOF', 'FKB', 'NOC', 'NAP', 'PMF','GOA', 'NYO', 'FNI', 'PSR', 'NUE', 'NTE', 'RZE', 'GOT', 'LTN','PGF', 'TER', 'MUC', 'HRK', 'ODS', 'VIT', 'MMX', 'XRY', 'ZAZ','MAH', 'BLL', 'SZZ', 'TFN', 'LIL', 'KIR', 'HAM', 'AMS', 'BOH','REU', 'LUX', 'BHD', 'BOJ', 'LPA', 'RAK', 'VGO', 'TUF', 'VLL','STR', 'CCF', 'OUD', 'MST', 'GLA', 'BIQ', 'TGD', 'SNN', 'TSR','KUN', 'TXL', 'LIG', 'AQJ', 'DLE', 'TNG', 'PDV', 'BRQ', 'EGC','ARN', 'EFL', 'BRE', 'JTR', 'CIY', 'HER', 'RHO', 'HEL', 'SEN','CHQ', 'RMI', 'VAR', 'CUF', 'SZG', 'ZAD', 'PIK', 'JMK', 'FEZ','DUS', 'NQY', 'PIS', 'SXB', 'KGS', 'CWL', 'XCR', 'OSL', 'CRV','WAW', 'FUE', 'BIO', 'NCE', 'LCJ', 'PUY', 'LUZ', 'SZY', 'AYT','CDT', 'AMM', 'TFS', 'LEI', 'LDE', 'AGA', 'BZG', 'KSC', 'BNX','LRH', 'BFS', 'PLQ', 'SBZ', 'AOI', 'INI', 'RJK', 'SCV', 'FMO','EXT', 'OMR', 'RMU', 'KLX', 'ABZ', 'RDZ', 'AAR', 'FSC', 'DLM','PED', 'CFE', 'TIA', 'AAL', 'DNR', 'VXO', 'GNB', 'LPP', 'ERF','BEY', 'CLJ', 'OSR', 'BSL', 'MME', 'DBV', 'VST', 'BVE', 'JSI','LCA', 'OZZ', 'PVK', 'DRS', 'SPC', 'TMP', 'SFT', 'LDY', 'TTU','KHE', 'ADB', 'HAJ', 'HAU', 'FDH', 'SPU', 'LLA', 'FNC', 'KLU' ))
            df.append(Departure_location)

            Arrival_location = col[1].selectbox(' Arrival location',
            ('BUD', 'MLA', 'CGN', 'KTW', 'AGP', 'BER', 'BRI', 'BCN', 'KRK','TLS', 'MRS', 'FEZ', 'OSL', 'NRN', 'PDL', 'MAD', 'CTA', 'SOF','LGW', 'SKG', 'TRF', 'GDN', 'OPO', 'EDI', 'SDR', 'FRA', 'STN','SVQ', 'AOI', 'MMX', 'CIA', 'FCO', 'BLQ', 'SZZ', 'NOC', 'AMS','VNO', 'RIX', 'NAP', 'PFO', 'SXF', 'KUN', 'WMI', 'BOD', 'VCE','PVK', 'TRN', 'PMO', 'KBP', 'BGY', 'INI', 'MAN', 'ALC', 'ACE','PMI', 'PIK', 'CFU', 'CPH', 'SCQ', 'LPA', 'DUB', 'CRL', 'LUX','AAR', 'WRO', 'SNN', 'LBA', 'HEL', 'PSA', 'RZE', 'BVA', 'VIE','RAK', 'FMM', 'SUF', 'MXP', 'MAH', 'NTE', 'KSC', 'RHO', 'LIS','ATH', 'BHX', 'BDS', 'BRE', 'BRU', 'TSF', 'HER', 'TER', 'CAG','TFS', 'EGC', 'VLC', 'BIQ', 'AMM', 'SEN', 'BRS', 'EMA', 'VIT','FAO', 'RMI', 'NYO', 'PSR', 'TNG', 'BTS', 'OTP', 'ORK', 'LPL','ZAD', 'POZ', 'TUF', 'EIN', 'PEG', 'BOH', 'LIG', 'DTM', 'RBA','GOT', 'MME', 'KIR', 'TPS', 'IBZ', 'KGS', 'NUE', 'VRN', 'FKB','FUE', 'TLL', 'AHO', 'ARN', 'PRG', 'LPP', 'HAM', 'XRY', 'OUD','MUC', 'PDV', 'LTN', 'BNX', 'DLE', 'TLV', 'TFN', 'LWO', 'SZG','GRO', 'HHN', 'LEI', 'EFL', 'GLA', 'NCL', 'BZG', 'ZTH', 'BLL','FSC', 'CUF', 'RMU', 'STR', 'ABZ', 'GOA', 'LCJ', 'PLQ', 'CRV','LRH', 'BFS', 'SZY', 'PGF', 'LDE', 'TXL', 'NDR', 'CHQ', 'CCF','CFE', 'XCR', 'JTR', 'PUY', 'TGD', 'RVN', 'VLL', 'AYT', 'ZAG','VGO', 'ODS', 'BES', 'CLJ', 'MST', 'VST', 'ZAZ', 'LIL', 'BZR','NCE', 'CIY', 'TSR', 'TRS', 'JSI', 'OMR', 'FNI', 'FMO', 'SPU','DRS', 'DNR', 'WAW', 'GNB', 'REU', 'VXO', 'VAR', 'DBV', 'LDY','NQY', 'ESU', 'CWL', 'DUS', 'BHD', 'BRQ', 'SCV', 'JMK', 'BOJ','PED', 'HRK', 'AGA', 'TIA', 'HAU', 'KLX', 'SBZ', 'LCA', 'AAL','EXT', 'OZZ', 'PMF', 'OSR', 'ERF', 'SXB', 'BVE', 'LUZ', 'PIS','AQJ', 'FNC', 'TMP', 'BIO', 'TTU', 'RDZ', 'HAJ', 'CDT', 'SFT','BSL', 'KHE', 'ADB', 'KUT', 'RJK', 'KLU', 'BEY', 'BEG', 'EVN','LYS', 'FDH', 'LLA', 'MPL', 'SPC', 'DLM'))
            df.append(Arrival_location)
            ScheduledRoute = Departure_location+"-"+Arrival_location # This could be deleted if conditions are removed

            col = st.columns(4)
            Departure_Scheduled_date = col[0].date_input('Departure Time Scheduled (y/m/d)', datetime.date(2022, 1, 24))
            Departure_Scheduled_time= col[1].time_input('Departure Time Scheduled (h/m)', datetime.time(8, 45, 1))
            df.append(datetime.datetime.combine(Departure_Scheduled_date, Departure_Scheduled_time)) # DepartureScheduled
            Arrival_Scheduled_date = col[2].date_input('Arrival Time Scheduled (y/m/d)', datetime.date(2022, 1, 24))
            Arrival_Scheduled_time = col[3].time_input('Arrival Time Scheduled (h/m)', datetime.time(8, 45, 1))
            df.append(datetime.datetime.combine(Arrival_Scheduled_date, Arrival_Scheduled_time)) # ArrivalScheduled

            col = st.columns(1)
            BlockTimeScheduled = col[0].slider('Block Time Scheduled in minutes',25, 355, 25)
            df.append(BlockTimeScheduled)

            col = st.columns(3)
            Adults = col[0].slider('Number Of Adults',0, 198, 0)
            Children= col[1].slider('Number Of Children',0, 198, 0)
            Infants = col[2].slider('Number Of Infants', 0, 198, 0) 
            df.append(Adults)
            df.append(Children)
            df.append(Infants)

            col = st.columns(2)
            Bags = col[0].text_input('Number Of Bags', '0')
            Freight = col[1].text_input('Weight Of Freight in kg', '0')
            df.append(Bags)
            df.append(Freight)
            submitted = st.form_submit_button(label="Submit")


        # load the data set 
        dff = load_dataset()
        if submitted:
            #if checking_input(AircraftCapacity, Adults, Children, ScheduledRoute, ServiceDescription):
            col1, col2 = st.columns([1, 3])

            df2 = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon'])
            # Define your javascript

            #color of map routes
            rgb = [241, 201, 50, 180]
            lat_long= pd.read_csv("data/GlobalAirportDatabase.txt", sep=",")

            data = {'origin': [Departure_location],
            'destination': [Arrival_location],
            'origin_lat': [lat_long[lat_long['iata']==Departure_location]['latitude'].values[0]],
            'origin_long': [lat_long[lat_long['iata']==Departure_location]['longitude'].values[0]],
            'dest_lat':[lat_long[lat_long['iata']==Arrival_location]['latitude'].values[0]], 
            'dest_long':[lat_long[lat_long['iata']==Arrival_location]['longitude'].values[0]],

            }
            # Create DataFrame
            airports = pd.DataFrame(data)
            latitude = float(airports['origin_lat'].values[0])
            longitude = float(airports['origin_long'].values[0])
            latitude_arrival= float(lat_long[lat_long['iata']==Arrival_location]['latitude'].values[0])
            longitude_arrival= float(lat_long[lat_long['iata']==Arrival_location]['longitude'].values[0])
            with col2:
                tab1, tab2 = st.tabs(["2D", "3D"])
                with tab1:
                    #layer of just the coordinate of each airport. Will always show. 
                    base_layer = pdk.Layer(
                        "ScatterplotLayer",
                        airports[['origin_long', 'origin_lat']],
                        opacity=0.8,
                        stroked=True,
                        filled=True,
                        radius_min_pixels=2,
                        radius_max_pixels=100,
                        line_width_min_pixels=1,
                        get_position=['origin_long','origin_lat'],
                        get_fill_color=[241, 201, 50],
                        get_line_color=[241, 201, 50],
                        wrapLongitude= True
                    )
                    #Layer of the air routes, will be filtered by user inputs
                    arc_layer = pdk.Layer(
                        "ArcLayer",
                        data=airports[['origin_lat', 'origin_long', 'dest_lat', 'dest_long']],
                        get_width = 8,
                        get_source_position=['origin_long', 'origin_lat'],
                        get_target_position=['dest_long', 'dest_lat'],
                        get_source_color=rgb,
                        get_target_color=rgb,
                        pickable=True, 
                        auto_highlight=True, 
                        tooltip=True,
                        wrapLongitude= True)


                    #text that shows up when somebody rolls over a route on the map
                    tooltip_text = {
                        "html": f" Scheduled-Route:    {Departure_location} - {Arrival_location}",
                        "style": {"backgroundColor":"white",
                                "color":"darkcyan"}}
                    latitude = float(airports['origin_lat'].values[0])
                    longitude = float(airports['origin_long'].values[0])
                    latitude_arrival= lat_long[lat_long['iata']==Arrival_location]['latitude'].values[0]
                    longitude_arrival= lat_long[lat_long['iata']==Arrival_location]['longitude'].values[0]
                    #initial view of the map. slightly tilted using pitch, and centered on Chad
                    view_state = pdk.ViewState(pitch=45, zoom = 4.7, latitude = latitude-3, longitude = longitude-3)

                    #create the entire map with both layers
                    deckchart = st.pydeck_chart(pdk.Deck(layers=[base_layer, arc_layer],
                                                        map_provider= 'mapbox',
                                                        map_style="mapbox://styles/raymazmaz/cl9owybd4005i16nulsvc1f4u",
                                                        initial_view_state= view_state,
                                                        tooltip=tooltip_text))
                with tab2:
                    ifr1=f'http://bayesgenes.moroccomfort.com/animation.html?Dlat={latitude}&Dlong={longitude}&Alat={latitude_arrival}&Along={longitude_arrival}'
                    components.iframe(src=ifr1,height=600, scrolling=True)

            with col1:
                    # Wrapt the javascript as html code
                complete_df = update_df(df)
                model = load_model()
                prediction=str(model.predict(complete_df)[0][0])
                distance= round(get_distance(Departure_location, Arrival_location),2)
                co2 = round(float(prediction)/69, 2)
                opt = round(3.6*co2,2)
                # Uncoment the section below if iframe is not working
                """ 
                st.markdown("#### Teledyne Ramp Weight")
                st.markdown(f"## {prediction} kg")
                st.markdown('')
                st.markdown('')
                st.markdown("#### CO2 Reduction")
                st.markdown(f"## {co2} Kg")
                st.markdown('')
                st.markdown('')
                st.markdown("####  Extra Fuel Optimisation")
                st.markdown(f"## {opt} kg")
                st.markdown('')
                st.markdown('')
                st.markdown("#### Distance traveled")
                st.markdown(f"## {distance} Km")"""
                ifr=f'http://bayesgenes.moroccomfort.com//test.html?TeledyneRampWeight={prediction}&CO2={co2}&optimisation={opt}&distance={distance}'
                components.iframe(src=ifr,height=700, scrolling=True)


            #st.write('Aircraft registration is', Bags)
            #account = searchconsole.authenticate(client_config="GSCTatieLouCredentials.json", serialize='credentials.json', flow="console")
            #st.write(account)