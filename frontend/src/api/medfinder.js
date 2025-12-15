/**
 * MedFinder API Client
 * 
 * Functions to interact with the Flask backend API
 */

const API_BASE = '/api';

/**
 * Search medicines by active ingredient
 * @param {string} ingredient - Active ingredient name (e.g., "Paracetamol")
 * @param {number} maxResults - Maximum number of results
 * @returns {Promise<Object>} Search results with statistics
 */
export const searchByIngredient = async (ingredient, maxResults = 20) => {
    const response = await fetch(`${API_BASE}/search/ingredient`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredient, max_results: maxResults }),
    });
    return response.json();
};

/**
 * Search medicines by composition with optional dosage filter
 * @param {string} formula - Chemical formula
 * @param {string} dosageFilter - Optional dosage filter (e.g., "500mg")
 * @param {number} maxResults - Maximum number of results
 * @returns {Promise<Object>} Search results with available dosages
 */
export const searchByComposition = async (formula, dosageFilter = null, maxResults = 20) => {
    const response = await fetch(`${API_BASE}/search/composition`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            formula,
            dosage_filter: dosageFilter,
            max_results: maxResults
        }),
    });
    return response.json();
};

/**
 * Get autocomplete suggestions for medicine search
 * @param {string} query - Partial search query
 * @param {number} maxSuggestions - Maximum suggestions
 * @returns {Promise<Object>} Medicine and composition suggestions
 */
export const getAutocomplete = async (query, maxSuggestions = 10) => {
    if (!query || query.length < 2) {
        return { success: true, medicines: [], compositions: [] };
    }

    const response = await fetch(`${API_BASE}/autocomplete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, max_suggestions: maxSuggestions }),
    });
    return response.json();
};

/**
 * Multi-field search across name, brand, composition, categories
 * @param {string} query - Search query
 * @param {number} maxResults - Maximum results
 * @returns {Promise<Object>} Search results
 */
export const multiFieldSearch = async (query, maxResults = 20) => {
    const response = await fetch(`${API_BASE}/search/multi`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, max_results: maxResults }),
    });
    return response.json();
};

/**
 * Fuzzy search with typo tolerance
 * @param {string} query - Search query (possibly misspelled)
 * @param {number} maxResults - Maximum results
 * @returns {Promise<Object>} Results with correction info
 */
export const fuzzySearch = async (query, maxResults = 10) => {
    const response = await fetch(`${API_BASE}/search/fuzzy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, max_results: maxResults }),
    });
    return response.json();
};

/**
 * Find similar medicines with savings information
 * @param {string} medicineName - Reference medicine name
 * @param {number} maxResults - Maximum alternatives
 * @returns {Promise<Object>} Reference medicine and alternatives with savings
 */
export const getSimilarMedicines = async (medicineName, maxResults = 10) => {
    const response = await fetch(`${API_BASE}/similar-medicines`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ medicine_name: medicineName, max_results: maxResults }),
    });
    return response.json();
};

/**
 * Check medicine availability on dawaai.pk
 * @param {string} medicineName - Medicine name
 * @returns {Promise<Object>} Availability status
 */
export const checkAvailability = async (medicineName) => {
    const response = await fetch(`${API_BASE}/check-availability`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ medicine_name: medicineName }),
    });
    return response.json();
};

/**
 * Get available dosages for an ingredient
 * @param {string} ingredient - Ingredient name
 * @returns {Promise<Object>} List of available dosages
 */
export const getAvailableDosages = async (ingredient) => {
    const response = await fetch(`${API_BASE}/dosages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredient }),
    });
    return response.json();
};

/**
 * Get medicine details by name
 * @param {string} medicineName - Medicine name
 * @returns {Promise<Object>} Medicine details
 */
export const getMedicineDetails = async (medicineName) => {
    const response = await fetch(`${API_BASE}/medicine/${encodeURIComponent(medicineName)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
};

/**
 * Get database statistics
 * @returns {Promise<Object>} Stats including total medicines, brands, etc.
 */
export const getStats = async () => {
    const response = await fetch(`${API_BASE}/stats`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
};

/**
 * Health check for API
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
    const response = await fetch(`${API_BASE}/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
};
