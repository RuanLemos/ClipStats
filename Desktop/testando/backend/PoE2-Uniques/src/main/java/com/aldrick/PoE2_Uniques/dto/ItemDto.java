package com.aldrick.PoE2_Uniques.dto;

import com.aldrick.PoE2_Uniques.entity.ItemType;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ItemDto {
    private Long id;
    private ItemType type_id;
    private String name;
}
