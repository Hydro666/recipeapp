export default class RecipeClient {

    constructor(
        private readonly baseUrl: string
    ) {}

    public async listRecipes() {
        let uri = new URL('/recipes', this.baseUrl);
        let response = await fetch(uri);
        let json = await response.json();
        return json;
    }

    public async getRecipe(name: string) {
        let uri = new URL(`/recipe/${name}`, this.baseUrl);
        let response = await fetch(uri);
        let json = await response.json();
        return json;
    }

}