package com.aldrick.PoE2_Uniques.mapper;

import com.aldrick.PoE2_Uniques.dto.ItemTypeDto;
import com.aldrick.PoE2_Uniques.entity.ItemType;

public class ItemTypeMapper {
    public static ItemTypeDto mapToItemDto(ItemType itemType){
        return new ItemTypeDto(
                itemType.getId(), itemType.getName()
        );
    }

    public static ItemType mapToItem(ItemTypeDto itemTypeDto){
        return new ItemType(
                itemTypeDto.getId(), itemTypeDto.getName()
        );
    }
}