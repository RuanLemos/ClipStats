import './App.css'
import FooterComponent from './components/FooterComponent'
import HeaderComponent from './components/HeaderComponent'
import ItemComponent from './components/ItemComponent'
import ListItemComponent from './components/ListItemComponent'
import {BrowserRouter, Routes, Route} from 'react-router-dom'

function App() {
  return (
    <>
      <BrowserRouter>
        <HeaderComponent />
        <Routes>
          {/* http://localhost:3000 */}
          <Route path='/' element = {<ListItemComponent />}></Route>
          
          {/* http://localhost:3000/items */}
          <Route path='/items' element = {<ListItemComponent />}></Route>

          {/* http://localhost:3000/add-item */}
          <Route path='/add-item' element = {<ItemComponent />}></Route>

          {/* http://localhost:3000/edit-item/1 */}
          <Route path='/edit-item/:id' element = {<ItemComponent />}></Route>
        </Routes>
        <FooterComponent />
      </BrowserRouter>
    </>
  )
}

export default App
