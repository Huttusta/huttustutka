import "./assets/css/style.css";
import {
  createMap,
  initInfoWindow,
  initMarkers,
  MarkerStorage,
  setProductChangeHandler,
} from "./map";

const API_URL = import.meta.env.VITE_API_URL;
const AMOUNTS_URL = `${API_URL}/amounts`
const DEFAULT_PRODUCT_ID = "003732";

// global storage
let markers: MarkerStorage;
let infoWindow: google.maps.InfoWindow;

const map = await createMap();
infoWindow = initInfoWindow();
markers = await initMarkers(map, infoWindow, AMOUNTS_URL, DEFAULT_PRODUCT_ID);
setProductChangeHandler(map, markers, infoWindow, AMOUNTS_URL)
