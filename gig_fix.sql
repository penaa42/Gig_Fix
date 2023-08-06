-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema gig_fix
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema gig_fix
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gig_fix` DEFAULT CHARACTER SET utf8 ;
USE `gig_fix` ;

-- -----------------------------------------------------
-- Table `gig_fix`.`bands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gig_fix`.`bands` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `city` VARCHAR(45) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gig_fix`.`charts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gig_fix`.`charts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `key` VARCHAR(45) NOT NULL,
  `time_signature` VARCHAR(45) NOT NULL,
  `tempo` INT NOT NULL,
  `band_id` INT NOT NULL,
  PRIMARY KEY (`id`, `band_id`),
  INDEX `fk_charts_bands1_idx` (`band_id` ASC) VISIBLE,
  CONSTRAINT `fk_charts_bands1`
    FOREIGN KEY (`band_id`)
    REFERENCES `gig_fix`.`bands` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gig_fix`.`musicians`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gig_fix`.`musicians` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `genre` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `experience` INT NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `instrument` VARCHAR(45) NOT NULL,
  `band_id` INT NOT NULL,
  PRIMARY KEY (`id`, `band_id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  INDEX `fk_musicians_bands1_idx` (`band_id` ASC) VISIBLE,
  CONSTRAINT `fk_musicians_bands1`
    FOREIGN KEY (`band_id`)
    REFERENCES `gig_fix`.`bands` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gig_fix`.`songs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gig_fix`.`songs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `musician_id` INT NOT NULL,
  PRIMARY KEY (`id`, `musician_id`),
  INDEX `fk_songs_musicians_idx` (`musician_id` ASC) VISIBLE,
  CONSTRAINT `fk_songs_musicians`
    FOREIGN KEY (`musician_id`)
    REFERENCES `gig_fix`.`musicians` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
