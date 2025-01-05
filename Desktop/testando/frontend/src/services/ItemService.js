import axios from "axios";

const REST_API_BASE_URL = 'http://localhost:8080/api/items'

export const listItems = () => axios.get(REST_API_BASE_URL);

export const createItem = (item) => axios.post(REST_API_BASE_URL, item);

export const getItem = (id) => axios.get(REST_API_BASE_URL + '/' + id);

export const updateItem = (item, id) => axios.put(REST_API_BASE_URL + '/' + id, item)

export const deleteItem = (id) => axios.delete(REST_API_BASE_URL + '/' + id)