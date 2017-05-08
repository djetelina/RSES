INSERT INTO ingredient_type VALUES ('legume');
INSERT INTO ingredient_type VALUES ('pastry');
INSERT INTO ingredient_type VALUES ('dairy');
INSERT INTO ingredient_type VALUES ('vegetable');
INSERT INTO ingredient_type VALUES ('fruit');

INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('milk', 'l', 'dairy', 1, 0.25, 7);
INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('yoghurt', 'cup', 'dairy', 2.0, 1.0, 20);
INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('black beans', 'can', 'legume', 3.0, 1.0, 350);
INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('roll', 'pc', 'pastry', 4.0, 2.0, 2);
INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('cucumber', 'pc', 'vegetable', 1.0, 0.3, 7);
INSERT INTO ingredient (id, unit, ingredient_type, suggestion_threshold, rebuy_threshold, durability)
VALUES ('banana', 'pc', 'fruit', 1.0, 1.0, 7);

INSERT INTO stock (ingredient, amount, amount_left, expiration_date, price)
VALUES ('milk', 2, 2, NULL, 12.90);
INSERT INTO stock (ingredient, amount, amount_left, expiration_date, price)
VALUES ('cucumber', 1, 1, NULL, 18.00);
INSERT INTO stock (ingredient, amount, amount_left, expiration_date, price)
VALUES ('black beans', 4, 4, '2018-02-20', 38.90);
INSERT INTO stock (ingredient, amount, amount_left, expiration_date, price)
VALUES ('roll', 10, 8, NULL, 2.20);

INSERT INTO recipe_category (id) VALUES ('main meal');
INSERT INTO recipe_category (id) VALUES ('breakfast');
INSERT INTO recipe_category (id) VALUES ('appetiser');
INSERT INTO recipe_category (id) VALUES ('dessert');
INSERT INTO recipe_category (id) VALUES ('snack');

INSERT INTO recipe (id, directions, picture, prepare_time, portions)
VALUES ('Roll with yoghurt', 'You know what to do :)',
        'http://vignette2.wikia.nocookie.net/theflophouse/images/0/05/Yogurt.jpg/revision/latest?cb=20130318225705',
        2, 1);

INSERT INTO categorized_recipes (recipe, category) VALUES ('Roll with yoghurt', 'breakfast');

INSERT INTO recipe_ingredients (recipe, ingredient, amount) VALUES ('Roll with yoghurt', 'roll', 1);
INSERT INTO recipe_ingredients (recipe, ingredient, amount) VALUES ('Roll with yoghurt', 'yoghurt', 1);
