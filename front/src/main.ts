import "./assets/css/style.css";
import {
  createMap,
  initInfoWindow,
  initMarkers,
  MarkerStorage,
  addProductSelectorOnChange,
} from "./map";

const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;
const MAP_ID = "map";
const APP_ID = "app";
const API_URL = import.meta.env.VITE_API_URL;
const AMOUNTS_URL = `${API_URL}/amounts`;

// global storage
let markers: MarkerStorage;
let infoWindow: google.maps.InfoWindow;

const map = await createMap(APP_ID, MAP_ID, GOOGLE_API_KEY);
infoWindow = initInfoWindow();
markers = await initMarkers(map, infoWindow, AMOUNTS_URL);
addProductSelectorOnChange(map, infoWindow, markers, AMOUNTS_URL);
