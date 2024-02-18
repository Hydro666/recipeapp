export class RecipeClient {

    constructor(
        private readonly baseUrl: string
    ) {}

    public async listRecipes() {
        let uri = new URL('/recipes', this.baseUrl);
        let response = await fetch(uri);
        let json = await response.json();
        return json;
    }

}