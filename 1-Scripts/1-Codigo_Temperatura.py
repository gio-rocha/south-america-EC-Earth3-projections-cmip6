                            #SCRIPT PARA TEMPERATURA

######### IMPORTANDO BIBLIOTETCAS #############
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader


#-------------------------------------- EC-EARTH3 no futuro -----------------------------------------------------

# caminhos
pathin = '/content/Dados/EC-EARTH3/'

#Abrindo os arquivos desejados
ssp2_arq = xr.open_dataset(pathin + 'nome-do-arquivo-ssp2.nc')

ssp5_arq = xr.open_dataset(pathin + 'nome-do-arquivo-ssp5.nc')

#CORES -----------------------------------------------
#Escolhendo a fonte
fonte_gl={'family':'Arial','size': 16, 'color': 'black'}

cbar_kwargs={'orientation':'horizontal','fraction':0.045,'pad':0.01,'extend':'neither'}

# Selecionando os dados da escala (início, fim, intervalo)
escala_temp=np.arange(0.5,7.5,0.5)

tick_temp=np.arange(0.5,7.5,0.5)

colors_temp= ['#fcdb88','#f6ca5d','#f2b317','#f7a975','#f27724','#cf5d11','#fbbcbc','#f98f8f','#f54444','#f21515','#d27a7a','#be4141','#960e0e']

cmap_temp= ListedColormap(colors_temp)

#Estabelecendo, respectivamente, a cor do topo e da base da barra
cmap_temp.set_over('#5a0808') #cor: vermelho

cmap_temp.set_under('#ffebb8')   #cor: azul claro

label = 'ºC' #unidade que aparecerá acima da barra com a escala selecionada

#SSP2-----------------------------------------------------------------------------------------------------------
#Variável que seleciona latitude, longitude e intervalo de tempo de acordo com os dados de temperatura
temp_ssp2= ssp2_arq.sel(lat=slice(-60,15),lon=slice(275,330), time=slice('2081','2100'))

#Selecionando os dados de temperatura, e convertendo de Kelvin para ºC
conversao_ssp2= temp_ssp2['tas'] - 273.15

#Calculando a média temporal
media_futuro_ssp2= conversao_ssp2.mean(dim='time')

#SSP5-----------------------------------------------------------------------------------------------------------
#Repetindo o mesmo procedimento para o ssp5
temp_ssp5= ssp5_arq.sel(lat=slice(-60,15),lon=slice(275,330), time=slice('2081','2100'))

conversao_ssp5= temp_ssp5['tas'] - 273.15

media_futuro_ssp5= conversao_ssp5.mean(dim='time')

#--------------------------------- Historical do EC-EARTH3 --------------------------------
#Abrindo o arquivo para o clima presente
hist = xr.open_dataset(pathin + 'nome-do-arquivo-historical.nc')

#Selecionando os dados de temperatura, as coordenadas para AS, e o recorte temporal para o clima presente
temp_hist= hist['tas'].sel(lat=slice(-60,15),lon=slice(275,330), time=slice('1995','2014'))

#conversão de Kelvin para ºC
conversao_hist= temp_hist - 273.15

#Calculando a média temporal
media_hist = conversao_hist.mean(dim='time')

#------------------------------------- MUDANÇA-------------------------------
#Calculando a mudança na temperatura de acordo com o SSP2
dif_ssp2= media_futuro_ssp2 - media_hist

#Calculando a mudança na temperatura de acordo com o SSP5
dif_ssp5 = media_futuro_ssp5 - media_hist

#CRIANDO A FIGURA------------------------------------------------------------
# Determinando tamanho e projeção dos dois mapas
fig,ax= plt.subplots(1, 2, figsize=(12,7.5),subplot_kw=dict(projection=ccrs.PlateCarree()))

#MAPA SSP2-------------------------------------------------------------
ssp2_mapa = ax[0].contourf(dif_ssp2.lon, dif_ssp2.lat, dif_ssp2, cmap=cmap_temp, levels=escala_temp, extend='both', transform=ccrs.PlateCarree())

ax[0].coastlines() #linhas da costa da AS

ax[0].add_feature(cfeature.BORDERS, linewidth=1) #linhas das fronteiras da AS

ax[0].add_feature(cfeature.STATES, edgecolor='black', linewidth=1) #linhas dos estados brasileiros

ax[0].set_title("SSP2-4.5", fontweight= 'bold', fontsize= 14)
#título que aparecerá acima do mapa à esquerda

#MAPA SSP5-------------------------------------------------------------
ssp5_mapa = ax[1].contourf(dif_ssp5.lon, dif_ssp5.lat, dif_ssp5, cmap=cmap_temp, levels=escala_temp, extend='both', transform=ccrs.PlateCarree())

ax[1].coastlines() #linhas da costa da AS

ax[1].add_feature(cfeature.BORDERS, linewidth=1) #linhas das fronteiras da AS

ax[1].add_feature(cfeature.STATES, edgecolor='black', linewidth=1) #linhas dos estados brasileiros

ax[1].set_title("SSP5-8.5", fontweight= 'bold', fontsize= 14)
#título que aparecerá acima do mapa à direita


for a in ax:
  #Adicionando o shape em cada mapa
  a.add_geometries(Reader('/content/Shapefiles/AR6_All_Regions_AS.shp').geometries(), ccrs.PlateCarree(),linewidth = 1.6, edgecolor = 'black', facecolor = 'none')

  #Colocando grade de coordenadas nas figuras
  fonte_gl_coord={'family':'serif', 'size':12,'color':'black'}
  gl=a.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,alpha=0)
  gl.top_labls=False ; gl.bottom_labels=True # Corrected: bootom_bals to bottom_labels
  gl.left_labels=True ; gl.right_labels=False
  gl.xpadding= 4 ; gl.ypadding=4
  gl.xlabel_style= fonte_gl_coord ; gl.ylabel_style= fonte_gl_coord

  # Escolhendo fonte para título
  plt.rcParams['font.family'] = 'Serif'

  plt.rcParams['axes.unicode_minus'] = False  #para aceitar os números negativos também


fig.suptitle('Mudança da Temperatura Média (ºC) entre 2081-2100 (EC-Earth3)', fontweight= 'bold', fontsize= 14, y=0.95)
#exemplo de título que ficará centralizado na figura

# Construção da barra que vai na lateral do mapa
cbar = fig.colorbar(ssp2_mapa,ax=ax, orientation='vertical', fraction=0.03,pad=0.04,ticks=tick_temp)

cbar.ax.set_title(label, fontsize=16)

cbar.ax.tick_params(labelsize=14, width=1, length=5)

pathout= '/content/Figuras/'

plt.savefig(pathout + 'nome-da-figura.png', dpi=300, bbox_inches= 'tight')

plt.show()
