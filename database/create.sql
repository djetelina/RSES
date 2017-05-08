DROP TABLE IF EXISTS shopping_list;
DROP TYPE IF EXISTS SHOPPING_STATUS;
DROP TABLE IF EXISTS recipe_made;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS categorized_recipes;
DROP TABLE IF EXISTS recipe_category;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS stock;
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS ingredient_type;


CREATE TABLE ingredient_type
(
  id VARCHAR(50) PRIMARY KEY
);
COMMENT ON TABLE ingredient_type IS 'Type of ingredient';

CREATE TABLE ingredient
(
  id VARCHAR(80) PRIMARY KEY,
  unit VARCHAR(10) NOT NULL,
  ingredient_type VARCHAR(50) NOT NULL,
  suggestion_threshold FLOAT DEFAULT 0.0,
  rebuy_threshold FLOAT DEFAULT 0.0,
  durability INT DEFAULT NULL,
  FOREIGN KEY (ingredient_type) REFERENCES ingredient_type (id) ON DELETE CASCADE
);
COMMENT ON TABLE ingredient IS 'Ingredient';
COMMENT ON COLUMN ingredient.durability IS 'Days before the ingredient expires if no expiration date is set';

CREATE TABLE stock
(
  ingredient VARCHAR(80),
  amount FLOAT NOT NULL,
  amount_left FLOAT NOT NULL,
  expiration_date DATE,
  time_bought TIMESTAMP DEFAULT NOW(),
  price FLOAT,
  FOREIGN KEY (ingredient) REFERENCES ingredient (id) ON DELETE CASCADE
);
COMMENT ON TABLE stock IS 'Stock of ingredients';

CREATE TABLE recipe
(
  id           VARCHAR(60) PRIMARY KEY,
  directions   TEXT NOT NULL,
  picture      VARCHAR(250),
  prepare_time INT,
  portions     INT  NOT NULL
);
COMMENT ON COLUMN recipe.prepare_time IS 'Time in minutes';

CREATE TABLE recipe_category
(
  id VARCHAR(20) PRIMARY KEY
);

CREATE TABLE categorized_recipes
(
  recipe VARCHAR(60),
  category VARCHAR(20),
  FOREIGN KEY (recipe) REFERENCES recipe (id) ON DELETE CASCADE,
  FOREIGN KEY (category) REFERENCES recipe (id) ON DELETE CASCADE,
  PRIMARY KEY (recipe, category)
);
COMMENT ON TABLE categorized_recipes IS 'What categories does a recipe belong to';

CREATE TABLE recipe_ingredients
(
  recipe VARCHAR(60),
  ingredient VARCHAR(80),
  amount FLOAT NOT NULL,
  FOREIGN KEY (recipe) REFERENCES recipe (id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient) REFERENCES ingredient (id) ON DELETE CASCADE,
  PRIMARY KEY (recipe, ingredient)
);
COMMENT ON TABLE recipe_ingredients IS 'Ingredients for a recipe';

CREATE TABLE recipe_made
(
  recipe    VARCHAR(60),
  time_made TIMESTAMP DEFAULT NOW(),
  portions  INT   NOT NULL,
  price     FLOAT NOT NULL,
  FOREIGN KEY (recipe) REFERENCES recipe (id) ON DELETE CASCADE
);
COMMENT ON TABLE recipe_made IS 'When was the recipe made, each recorded history';

CREATE TYPE SHOPPING_STATUS AS ENUM ('list', 'cart');
CREATE TABLE shopping_list
(
  ingredient    VARCHAR(80) PRIMARY KEY,
  wanted_amount FLOAT NOT NULL,
  status        SHOPPING_STATUS DEFAULT 'list',
  FOREIGN KEY (ingredient) REFERENCES ingredient (id) ON DELETE CASCADE
);
COMMENT ON TABLE shopping_list IS 'What needs to be bought'
