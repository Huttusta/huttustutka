import "./assets/css/style.css";
import {
  createMap,
  initInfoWindow,
  initMarkers,
  MarkerStorage,
  setProductChangeHandler,
} from "./map";
import { getProducts, Product } from "./util"

const API_URL = import.meta.env.VITE_API_URL;
const AMOUNTS_URL = `${API_URL}/amounts`
const DETAILS_URL = `${API_URL}/details`
const DEFAULT_PRODUCT_ID = "003732";
const ALKO_PRODUCTS = <Array<Product>>await getProducts()

// global storage
let markers: MarkerStorage;
let infoWindow: google.maps.InfoWindow;

const map = await createMap();
infoWindow = initInfoWindow();
markers = await initMarkers(map, infoWindow, AMOUNTS_URL, DETAILS_URL, DEFAULT_PRODUCT_ID);
setProductChangeHandler(map, markers, infoWindow, AMOUNTS_URL, DETAILS_URL, ALKO_PRODUCTS)
