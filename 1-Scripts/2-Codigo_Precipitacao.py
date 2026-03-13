#SCRIPT PARA PRECIPITAÇÃO

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
pathin = '/content/EC-EARTH3/'

#Abrindo os arquivos desejados
ssp2_arq = xr.open_dataset(pathin + 'nome-do-arquivo-ssp2.nc')

ssp5_arq = xr.open_dataset(pathin + 'nome-do-arquivo-ssp5.nc')

#CORES -----------------------------------------------
#Escolhendo a fonte
fonte_gl={'family':'Arial','size': 16, 'color': 'black'}


cbar_kwargs={'orientation':'horizontal','fraction':0.045,'pad':0.01,'extend':'neither'}

# Selecionando os dados da escala (início, fim, intervalo)
escala_pr=np.arange(-40,70,10)

tick_pr=np.arange(-40,70,10)

colors_pr= ['#653c1a','#846348','#b29e8d','#c8ac7b','#9aa2a4','#b8d4d0','#64c8b7','#54a297','#38837d','#06645c']

cmap_pr= ListedColormap(colors_pr)

#Estabelecendo, respectivamente, a cor do topo e da base da barra
cmap_pr.set_over('#00271e') #cor: verde escuro

cmap_pr.set_under('#371400')   #cor: marrom forte

label = '%' #unidade que aparecerá acima da barra com a escala

#SSP2-----------------------------------------------------------------------------------------------------------
#Variável que seleciona as coordenadas da AS, e o recorte temporal para o clima futuro
pr_ssp2= ssp2_arq.sel(lat=slice(-60,15),lon=slice(275,330), time=slice('2081','2100'))

#Selecionando os dados de temperatura, e convertendo de kg m-2 s-1 para mm/dia
conversao_ssp2= pr_ssp2['pr'] * 86400

#Calculando a média temporal
media_futuro_ssp2= conversao_ssp2.mean(dim='time')

#SSP5-----------------------------------------------------------------------------------------------------------
#Repete-se o mesmo procedimento para o SSP5
pr_ssp5= ssp5_arq.sel(lat=slice(-60,15),lon=slice(275,330), time=slice('2081','2100'))

conversao_ssp5= pr_ssp5['pr'] * 86400

media_futuro_ssp5= conversao_ssp5.mean(dim='time')


#--------------------------------- Historical do EC-EARTH3 --------------------------------
hist = xr.open_dataset(pathin + 'nome-arquivo-historical.nc')

pr_hist= hist['pr'].sel(lat=slice(-60,15),lon=slice(275,330), time=slice('1995','2014'))

conversao_hist= pr_hist * 86400

media_hist = conversao_hist.mean(dim='time')


#------------------------------------- MUDANÇA--------------------------------
#Calculando a mudança na precipitação e convertendo para percentual
dif_ssp2= ((media_futuro_ssp2 - media_hist) / media_hist ) * 100

dif_ssp5 = ((media_futuro_ssp5 - media_hist ) / media_hist) * 100


#CRIANDO A FIGURA------------------------------------------------------------
# Determinando tamanho e projeção dos dois mapas
fig,ax= plt.subplots(1, 2, figsize=(12,7.5),subplot_kw=dict(projection=ccrs.PlateCarree()))

#MAPA SSP2-------------------------------------------------------------
ssp2_mapa = ax[0].contourf(dif_ssp2.lon, dif_ssp2.lat, dif_ssp2, cmap=cmap_pr, levels=escala_pr, extend='both', transform=ccrs.PlateCarree())

ax[0].coastlines() #linhas da costa da AS

ax[0].add_feature(cfeature.BORDERS, linewidth=1) #linhas das fronteiras da AS

ax[0].add_feature(cfeature.STATES, edgecolor='black', linewidth=1) #linhas dos estados brasileiros

ax[0].set_title("SSP2-4.5", fontweight= 'bold', fontsize= 14)
#título que aparecerá acima do mapa à esquerda

#MAPA SSP5-------------------------------------------------------------
ssp5_mapa = ax[1].contourf(dif_ssp5.lon, dif_ssp5.lat, dif_ssp5, cmap=cmap_pr, levels=escala_pr, extend='both', transform=ccrs.PlateCarree())

ax[1].coastlines() #linhas da costa da AS

ax[1].add_feature(cfeature.BORDERS, linewidth=1) #linhas das fronteiras da AS

ax[1].add_feature(cfeature.STATES, edgecolor='black', linewidth=1) #linhas dos estados brasileiros

ax[1].set_title("SSP5-8.5", fontweight= 'bold', fontsize= 14)
#título que aparecerá acima do mapa à direita


for a in ax:
  #Adicionando o shape nos mapas
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


fig.suptitle('Mudança da Precipitação Total (%) entre 2081-2100 (EC-Earth3)', fontweight= 'bold', fontsize= 14, y=0.95)
#exemplo de título que aparecerá de forma centralizada na figura

# Construção da barra que vai na lateral do mapa
cbar = fig.colorbar(ssp2_mapa,ax=ax, orientation='vertical', fraction=0.03,pad=0.04,ticks=tick_pr)

cbar.ax.set_title(label, fontsize=16)

cbar.ax.tick_params(labelsize=14, width=1, length=5)

pathout= '/content/Figuras/'

plt.savefig(pathout + 'nome-da-figura.png', dpi=300, bbox_inches= 'tight')

plt.show()
