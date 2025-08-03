import React, { useState } from 'react';

const predefinedRecipes = {
  'chicken,tomato': `Chicken Tomato Delight
Ingredients:
- Chicken
- Tomato
- Salt
- Pepper

Instructions:
1. Cut chicken into pieces.
2. Chop tomatoes.
3. Cook chicken until brown.
4. Add tomatoes and cook until soft.
5. Season with salt and pepper.
6. Serve hot.`,
  'rice,egg': `Egg Fried Rice
Ingredients:
- Rice
- Egg
- Soy sauce
- Green onions

Instructions:
1. Cook rice and let cool.
2. Scramble eggs in a pan.
3. Add rice and soy sauce.
4. Stir fry with green onions.
5. Serve warm.`
};

function App() {
  const [ingredients, setIngredients] = useState('');
  const [recipe, setRecipe] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const searchRecipes = async () => {
    setError('');
    setRecipe('');
    const trimmedIngredients = ingredients.trim().toLowerCase();
    if (!trimmedIngredients) {
      setError('Please enter some ingredients.');
      return;
    }

    setLoading(true);

    // Check predefined recipes
    if (predefinedRecipes[trimmedIngredients]) {
      setRecipe(predefinedRecipes[trimmedIngredients]);
      setLoading(false);
      return;
    }

    // Call backend API
    try {
      const response = await fetch('/generate_recipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredients: trimmedIngredients.split(',').map(i => i.trim())
        })
      });
      const data = await response.json();
      if (data.status === 'success') {
        setRecipe(data.recipe);
      } else {
        setError(data.error || 'Failed to generate recipe.');
      }
    } catch (err) {
      setError('Error connecting to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'Arial, sans-serif' }}>
      <h1>IntelliRecipe</h1>
      <p>Enter ingredients separated by commas:</p>
      <input
        type="text"
        value={ingredients}
        onChange={e => setIngredients(e.target.value)}
        placeholder="e.g. chicken, tomato"
        style={{ width: '100%', padding: '0.5rem', fontSize: '1rem' }}
      />
      <button onClick={searchRecipes} disabled={loading} style={{ marginTop: '1rem', padding: '0.5rem 1rem' }}>
        {loading ? 'Loading...' : 'Find Recipes'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {recipe && (
        <pre style={{ whiteSpace: 'pre-wrap', marginTop: '1rem', backgroundColor: '#f0f0f0', padding: '1rem' }}>
          {recipe}
        </pre>
      )}
    </div>
  );
}

export default App;
