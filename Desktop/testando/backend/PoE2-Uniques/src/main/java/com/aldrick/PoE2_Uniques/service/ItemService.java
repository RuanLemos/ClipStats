package com.aldrick.PoE2_Uniques.service;

import com.aldrick.PoE2_Uniques.dto.ItemDto;

import java.util.List;

public interface ItemService {
    ItemDto createItem(ItemDto itemDto);
    ItemDto getItemById(Long id);
    List<ItemDto> getAllItems();
    ItemDto updateItem(Long id, ItemDto updatedItem);
    void deleteItem(Long id);
}