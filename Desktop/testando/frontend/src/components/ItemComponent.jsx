import React, { useEffect, useState } from 'react'
import { createItem, getItem, updateItem } from '../services/ItemService';
import { useNavigate, useParams } from 'react-router-dom'

const ItemComponent = () => {

    const [name, setName] = useState('')
    const [type_id, setType_id] = useState('')
    const navigator = useNavigate();
    
    const {id} = useParams();
    const [errors, setErrors] = useState({
        name: '',
        type_id:'',
    })

    useEffect(() => {
        if(id){
            getItem(id).then((response) => {
                setName(response.data.name);
                setType_id(response.data.type_id?.id?.toString());
            }).catch(error => {
                console.error(error);
            })
        }
    }, [id])
    //const handleName = (e) => setName(e.target.value);

    //const handleTypeId = (e) => setType_id(e.target.value);

    function saveItem(e){
        e.preventDefault();

        if(validateForm()){
            const item = {
                name,
                type_id: { id: parseInt(type_id) } //Making it an object with the id
            };
    
            console.log(item);
            
            if(id){
                updateItem(item, id).then((response) => {
                    console.log(response.data);
                    navigator('/items');
                })
            } else{
                createItem(item).then((response) => {
                    console.log(response.data);
                    navigator('/items');
                })
            }
        }
    }

    function validateForm(){
        let valid = true

        const errorsCopy = {... errors}

        if(name.trim()){
            errorsCopy.name = '';
        } else {
            errorsCopy.name = 'Name can not be empty lil bro';
            valid = false
        }

        if(type_id.trim()){
            errorsCopy.type_id = '';
        } else {
            errorsCopy.type_id = 'Category ID can not be empty, big man';
            valid = false
        }

        setErrors(errorsCopy);

        return valid;
    }

    function pageTitle(){
        if(id) {
            return <h2 className='text-center mt-3'>Update Item</h2>
        } else {
            return <h2 className='text-center mt-3'>Add Item</h2>
        }
    }

    return (
    <div className='container'>
        <div className='row mt-5'>
            <div className='card col-md-6 offset-md-3 offset-md-3'>
                {
                    pageTitle()
                }
                <div className='card-body'>
                    <form>
                        <div className='form-group mb-2'>
                            <label className='form-label'>Item Name:</label>
                            <input 
                                type="text" 
                                placeholder='Enter the items name' 
                                name='name' 
                                value={name} 
                                className={`form-control ${ errors.name ? 'is-invalid': ''}`} 
                                onChange={(e) => setName(e.target.value)}
                            />
                            {errors.name && <div className='invalid-feedback'>{errors.name}</div>}
                        </div>

                        <div className='form-group mb-2'>
                            <label className='form-label'>Category ID:</label>
                            <input 
                                type="text" 
                                placeholder='Enter the category id of the item' 
                                name='type_id' 
                                value={type_id} 
                                className={`form-control ${ errors.type_id ? 'is-invalid': ''}`} 
                                onChange={(e) => setType_id(e.target.value)}
                            />
                            {errors.type_id && <div className='invalid-feedback'>{errors.type_id}</div>}
                        </div>
                        <button className='btn btn-success' onClick={saveItem}>Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
  )
}

export default ItemComponent