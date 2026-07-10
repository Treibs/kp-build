module cookbook::recipes {
    use std::string::String;
    use std::vector;
    use sui::balance::{self, Balance};
    use sui::coin::{self, Coin};
    use sui::dynamic_field;
    use sui::event;
    use sui::object::{self, UID};
    use sui::sui::SUI;
    use sui::table::{self, Table};
    use sui::transfer;
    use sui::tx_context::{self, TxContext};

    const RECIPE_FEE: u64 = 1_000_000;
    const ErrInvalidRating: u64 = 1;
    const ErrAlreadyRated: u64 = 2;
    const ErrInsufficientFee: u64 = 3;

    public struct Recipe has store {
        id: u64,
        title: String,
        ingredient_count: u64,
        creator: address,
        total_rating: u64,
        rating_count: u64,
    }

    public struct RecipeBook has key {
        id: UID,
        recipes: Table<u64, Recipe>,
        next_recipe_id: u64,
        fee_pool: Balance<SUI>,
    }

    public struct AdminCap has key, store {
        id: UID,
    }

    public struct RecipeSubmitted has copy, drop {
        recipe_id: u64,
        title: String,
        creator: address,
    }

    public struct RecipeRated has copy, drop {
        recipe_id: u64,
        rating: u64,
        rater: address,
    }

    fun init(ctx: &mut TxContext) {
        let admin_cap = AdminCap {
            id: object::new(ctx),
        };

        let recipe_book = RecipeBook {
            id: object::new(ctx),
            recipes: table::new(ctx),
            next_recipe_id: 1,
            fee_pool: balance::zero<SUI>(),
        };

        transfer::transfer(admin_cap, tx_context::sender(ctx));
        transfer::share_object(recipe_book);
    }

    public fun submit_recipe(
        recipe_book: &mut RecipeBook,
        title: String,
        ingredient_count: u64,
        fee: Coin<SUI>,
        ctx: &mut TxContext,
    ): u64 {
        assert!(coin::value(&fee) >= RECIPE_FEE, ErrInsufficientFee);

        let recipe_id = recipe_book.next_recipe_id;
        recipe_book.next_recipe_id = recipe_book.next_recipe_id + 1;

        let recipe = Recipe {
            id: recipe_id,
            title,
            ingredient_count,
            creator: tx_context::sender(ctx),
            total_rating: 0,
            rating_count: 0,
        };

        table::add(&mut recipe_book.recipes, recipe_id, recipe);

        let ratings_map: Table<address, u64> = table::new(ctx);
        dynamic_field::add(&mut recipe_book.id, recipe_id, ratings_map);

        balance::join(&mut recipe_book.fee_pool, coin::into_balance(fee));

        event::emit(RecipeSubmitted {
            recipe_id,
            title,
            creator: tx_context::sender(ctx),
        });

        recipe_id
    }

    public fun rate_recipe(
        recipe_book: &mut RecipeBook,
        recipe_id: u64,
        rating: u64,
        ctx: &mut TxContext,
    ) {
        assert!(rating >= 1 && rating <= 5, ErrInvalidRating);

        let rater = tx_context::sender(ctx);

        let ratings_map: &mut Table<address, u64> = dynamic_field::borrow_mut(&mut recipe_book.id, recipe_id);
        assert!(!table::contains(ratings_map, rater), ErrAlreadyRated);
        table::add(ratings_map, rater, rating);

        let recipe: &mut Recipe = table::borrow_mut(&mut recipe_book.recipes, recipe_id);
        recipe.total_rating = recipe.total_rating + rating;
        recipe.rating_count = recipe.rating_count + 1;

        event::emit(RecipeRated {
            recipe_id,
            rating,
            rater,
        });
    }

    public fun get_average_rating(recipe_book: &RecipeBook, recipe_id: u64): u64 {
        let recipe = table::borrow(&recipe_book.recipes, recipe_id);
        if (recipe.rating_count == 0) {
            0
        } else {
            (recipe.total_rating * 100) / recipe.rating_count
        }
    }

    public fun get_recipe_info(recipe_book: &RecipeBook, recipe_id: u64): (&String, &u64, address, u64) {
        let recipe = table::borrow(&recipe_book.recipes, recipe_id);
        let average_rating = if (recipe.rating_count == 0) {
            0
        } else {
            (recipe.total_rating * 100) / recipe.rating_count
        };
        (&recipe.title, &recipe.ingredient_count, recipe.creator, average_rating)
    }

    public fun withdraw_fees(
        recipe_book: &mut RecipeBook,
        _admin_cap: &AdminCap,
        ctx: &mut TxContext,
    ): Coin<SUI> {
        let amount = balance::value(&recipe_book.fee_pool);
        coin::from_balance(balance::split(&mut recipe_book.fee_pool, amount), ctx)
    }
}
