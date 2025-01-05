package com.aldrick.PoE2_Uniques.repository;

import com.aldrick.PoE2_Uniques.entity.Item;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository<Item, Long> {

}
