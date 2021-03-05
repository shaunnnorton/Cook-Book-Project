from flask import Blueprint, request, render_template, redirect, url_for, flash
from recipe_app.main.forms import RecipeForm, IngredientForm, SearchForm
from recipe_app.models import Recipe, Ingredient, recipe_ingredient_association
from recipe_app.main.helpers import clean_input_to_list, manage_ingredients
from flask_login import login_required, current_user


from recipe_app import app, db


main = Blueprint('main', __name__)


@main.route('/',methods=['GET','POST'])
def homepage():
    """Homepage to be rendered on base route"""
    context = {
        'recipes':Recipe.query.all(),
        'ingredients':Ingredient.query.all()
    }

    return render_template('home.html',**context)


@main.route('/create-recipe',methods=['GET','POST'])
@login_required
def create_recipe():
    """Allows the user to create a recipe if they are authenticated"""
    recipe_form = RecipeForm()

    context = {
        'recipe_form':recipe_form
    }

    if recipe_form.validate_on_submit():
        recipe_ingredients = manage_ingredients(clean_input_to_list(recipe_form.ingredients.data))
        ingredient_amounts = recipe_form.ingredient_amounts.data.split(",")
        new_recipe = Recipe(
            title=recipe_form.title.data,
            description=recipe_form.description.data,
            servings=recipe_form.servings.data,
            instructions=recipe_form.instructions.data,
            image=recipe_form.image_url.data 
        )
        index=0
        for ingredient in recipe_ingredients:
            if index < len(ingredient_amounts):
                new_association = recipe_ingredient_association(amount=ingredient_amounts[index],ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            else:
                new_association = recipe_ingredient_association(amount='',ingredient=ingredient)
                new_recipe.ingredients.append(new_association)
            index += 1 

        db.session.add(new_recipe)
        db.session.commit()
        flash(f"Created New Recipe {new_recipe.title}")
        return redirect(url_for('main.view_recipe', recipe_id=new_recipe.id))

    return render_template('create_recipe.html',**context)

@main.route('/recipe/<recipe_id>')
def view_recipe(recipe_id):
    """Shows information for a recipe with given recipe id """
    recipe = Recipe.query.get(recipe_id)
    context = {
        "recipe":recipe
    }
    
    return render_template('recipe.html',**context)

@main.route('/ingredient/<ingredient_id>')
def view_ingredient(ingredient_id):
    """Shows All recipes with ingredient as and ingredient"""
    ingredient = Ingredient.query.get(ingredient_id)
    context = {
        'ingredient':ingredient
    }
    
    return render_template('ingredient.html', **context)




@main.route("/profile", methods=['GET',"POST"])
@login_required
def view_profile():
    """Shows the profile of the currently logged in user"""
    return render_template('profile.html')

@main.route('/search', methods=['GET','POST'])
def search():
    """Shows a page allowing for the searching of a recipe or ingredient"""
    form = SearchForm()
    if form.validate_on_submit():
        print('HELLO')
        
        recipe_results = Recipe.query.filter(Recipe.title.like(f'%{form.search_query.data}%')).all()
        ingredient_results = Ingredient.query.filter(Ingredient.name.like(f'%{form.search_query.data}%')).all()
        context = {
            'recipe_results':recipe_results,
            'ingredient_results':ingredient_results,
            'form':SearchForm(search_query=form.search_query.data)
        }
        print(context)
        return render_template('search.html', **context)
    
    
    return render_template('search.html', form=form)


@main.route('/favorite/<recipe_id>')
@login_required
def add_favorite(recipe_id):
    """Adds the recipe with given id the the current users favorites"""
    recipe=Recipe.query.get(recipe_id)
    current_user.favorite_recipes.append(recipe)
    db.session.commit()
    flash(f'You Have Favorited This Recipe!')
    return redirect(url_for('main.view_recipe',recipe_id=recipe_id))

@main.route('/unfavorite/<recipe_id>')
@login_required
def remove_favorite(recipe_id):
    """Removes the recipe with the given recipe_id from the current users favorites."""
    recipe=Recipe.query.get(recipe_id)
    if recipe in current_user.favorite_recipes:
        current_user.favorite_recipes.remove(recipe)
        db.session.commit()
    flash(f'You Have Unfavorited This Recipe!')
    return redirect(url_for('main.view_recipe',recipe_id=recipe_id))
