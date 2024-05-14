import folium
import json
import webbrowser

class Map:
    def __init__(self):
        self.locate=None        
        self.latitude=None
        self.longitude=None
        self.save_html_file='C:/Users/kmg01/Server/Graduate/crash.html'

    def read_data(self,data):
        parsed_data=json.loads(data)
        self.latitude=parsed_data['Latitude']
        self.longitude=parsed_data['Longitude']

    def show_map(self):       
        self.locate=folium.Map(location=[self.latitude,self.longitude],zoom_start=18)
        folium.Marker([self.latitude,self.longitude], popup='사고 발생 위치!').add_to(self.locate)        
        
        self.locate.save(self.save_html_file)
        webbrowser.open(self.save_html_file)