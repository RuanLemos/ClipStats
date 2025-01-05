package com.aldrick.PoE2_Uniques.service.implementation;

import com.aldrick.PoE2_Uniques.dto.ItemDto;
import com.aldrick.PoE2_Uniques.entity.Item;
import com.aldrick.PoE2_Uniques.exception.ResourceNotFoundException;
import com.aldrick.PoE2_Uniques.mapper.ItemMapper;
import com.aldrick.PoE2_Uniques.repository.ItemRepository;
import com.aldrick.PoE2_Uniques.service.ItemService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class ItemServiceImplementation implements ItemService {

    private ItemRepository itemRepository;

    @Override
    public ItemDto createItem(ItemDto itemDto) {
        Item item = ItemMapper.mapToItem(itemDto);
        Item savedItem = itemRepository.save(item);
        return ItemMapper.mapToItemDto(savedItem);
    }

    @Override
    public ItemDto getItemById(Long id) {
        Item item = itemRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("No items with that id were found"));
        return ItemMapper.mapToItemDto(item);
    }

    @Override
    public List<ItemDto> getAllItems() {
        List<Item> items = itemRepository.findAll();
        return items.stream().map(ItemMapper::mapToItemDto).toList();
    }

    @Override
    public ItemDto updateItem(Long id, ItemDto updatedItem) {
        Item item = itemRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("No items with that id were found"));
        item.setName(updatedItem.getName());
        item.setType_id(updatedItem.getType_id());

        Item updatedItemObj = itemRepository.save(item);
        return ItemMapper.mapToItemDto(updatedItemObj);
    }

    @Override
    public void deleteItem(Long id) {
        Item item = itemRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("No items with that id were found"));
        itemRepository.delete(item);
    }
}
