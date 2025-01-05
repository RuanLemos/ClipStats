import React, {useEffect, useState} from 'react'
import { deleteItem, listItems } from '../services/ItemService'
import { useNavigate } from 'react-router-dom'

const ListItemComponent = () => {

    const [items, setItems] = useState([])

    const navigator = useNavigate();
    /*
    useEffect(() =>{
        listItems().then((response) => {
            setItems(response.data);
        }).catch(error => {
            console.error(error)
        })

    }, [])
    */

    useEffect(() =>{
        getAllItems()
    }, [])

    function getAllItems(){
        listItems().then((response) => {
            const transformedItems = response.data.map(item => ({
                id: item.id,
                name: item.name,
                type: item.type_id.name, //Only the name of the item type is retrieved
            }));
            setItems(transformedItems);
        }).catch(error => {
            console.error(error)
        })
    }

    function addNewItem(){
        navigator('/add-item')
    }

    function updateItem(id){
        navigator(`/edit-item/${id}`)
    }

    function removeItem(id){
        deleteItem(id).then((response) => {
            getAllItems()
        }).catch(error => {
            console.error(error);
        })
    }
    
  return (
    <div className='container mt-5'>
        <h2 className='text-center mb-3'>PoE 2 Unique Items</h2>
        <button className='btn btn-primary mb-2' onClick={addNewItem}>Add Item</button>
        <table className='table table-striped table-bordered'>
            <thead>
                <tr>
                    <th>Item ID</th>
                    <th>Item Name</th>
                    <th>Item Category</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {
                    items.map(item =>
                        <tr key={item.id}>
                            <td>{item.id}</td>
                            <td>{item.name}</td>
                            <td>{item.type}</td>
                            <td>
                                <button className='btn btn-info' onClick={() => updateItem(item.id)}>Update</button>
                            </td>
                            <td>
                                <button className='btn btn-danger' onClick={() => removeItem(item.id)}>Delete</button>
                            </td>
                        </tr>
                    )
                }
                <tr>

                </tr>
            </tbody>
        </table>
    </div>
  )
}

export default ListItemComponent