package com.aldrick.PoE2_Uniques.controller;

import com.aldrick.PoE2_Uniques.dto.ItemTypeDto;
import com.aldrick.PoE2_Uniques.service.ItemTypeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/item_types")
public class ItemTypeController {

    @Autowired
    private ItemTypeService itemTypeService;

    @PostMapping
    public ResponseEntity<ItemTypeDto> createItemType(@RequestBody ItemTypeDto itemTypeDto){
        ItemTypeDto savedItemType = itemTypeService.createItemType(itemTypeDto);
        return new ResponseEntity<>(savedItemType, HttpStatus.CREATED);
    }
}
