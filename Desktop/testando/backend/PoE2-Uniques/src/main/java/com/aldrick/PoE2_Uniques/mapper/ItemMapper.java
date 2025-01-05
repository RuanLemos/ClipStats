package com.aldrick.PoE2_Uniques.mapper;

import com.aldrick.PoE2_Uniques.dto.ItemDto;
import com.aldrick.PoE2_Uniques.entity.Item;

public class ItemMapper {
    public static ItemDto mapToItemDto(Item item){
        return new ItemDto(
            item.getId(), item.getType_id(), item.getName()
        );
    }

    public static Item mapToItem(ItemDto item){
        return new Item(
                item.getId(), item.getType_id(), item.getName()
        );
    }
}
