package com.aldrick.PoE2_Uniques.controller;

import com.aldrick.PoE2_Uniques.dto.ItemDto;
import com.aldrick.PoE2_Uniques.service.ItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin("*")
@RestController
@RequestMapping("/api/items")
public class ItemController {

    @Autowired
    private ItemService itemService;

    //Build add Item REST API
    @PostMapping
    public ResponseEntity<ItemDto> createItem(@RequestBody ItemDto itemDto){ //@RequestBody to convert the JSON response into an ItemDto object
        ItemDto savedItem = itemService.createItem(itemDto);
        return new ResponseEntity<>(savedItem, HttpStatus.CREATED);
    }

    //Build get Item REST API
    @GetMapping("{id}")
    public ResponseEntity<ItemDto> getItemById(@PathVariable("id") Long id){//@PathVariable to bind id param to the @GetMapping id
        ItemDto itemDto = itemService.getItemById(id);
        return ResponseEntity.ok(itemDto);
    }

    //Build get all Items REST API
    @GetMapping
    public ResponseEntity<List<ItemDto>> getAllItems(){
        List<ItemDto> items = itemService.getAllItems();
        return ResponseEntity.ok(items);
    }

    //Build update Item REST API
    @PutMapping("{id}")
    public ResponseEntity<ItemDto> updateItem(@PathVariable("id") Long id, @RequestBody ItemDto updatedItem){
        ItemDto itemDto = itemService.updateItem(id, updatedItem);
        return ResponseEntity.ok(itemDto);
    }

    //Build delete Item REST API
    @DeleteMapping("{id}")
    public ResponseEntity<String> deleteItem(@PathVariable("id") Long id){
        itemService.deleteItem(id);
        return ResponseEntity.ok("Item successfully deleted");
    }
}