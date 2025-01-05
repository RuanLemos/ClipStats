package com.aldrick.PoE2_Uniques.service.implementation;

import com.aldrick.PoE2_Uniques.dto.ItemTypeDto;
import com.aldrick.PoE2_Uniques.entity.ItemType;
import com.aldrick.PoE2_Uniques.mapper.ItemTypeMapper;
import com.aldrick.PoE2_Uniques.repository.ItemTypeRepository;
import com.aldrick.PoE2_Uniques.service.ItemTypeService;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ItemTypeServiceImplementation implements ItemTypeService {

    private ItemTypeRepository itemTypeRepository;

    @Override
    public ItemTypeDto createItemType(ItemTypeDto itemTypeDto) {
        ItemType itemType = ItemTypeMapper.mapToItem(itemTypeDto);
        ItemType savedItemType = itemTypeRepository.save(itemType);
        return ItemTypeMapper.mapToItemDto(savedItemType);
    }
}
