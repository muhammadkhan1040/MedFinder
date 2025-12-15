/**
 * Format price for display
 * @param {string|number} price - Price value
 * @returns {string} Formatted price
 */
export const formatPrice = (price) => {
    if (!price) return 'N/A';

    // If already a string with Rs., return as is
    if (typeof price === 'string' && price.includes('Rs.')) {
        return price;
    }

    // Convert to number and format
    const numPrice = typeof price === 'string'
        ? parseFloat(price.replace(/[^0-9.]/g, ''))
        : price;

    if (isNaN(numPrice)) return 'N/A';

    return `Rs. ${numPrice.toFixed(2)}`;
};

/**
 * Extract numeric price from string
 * @param {string} priceStr - Price string (e.g., "Rs. 5.17/tablet")
 * @returns {number} Numeric price
 */
export const parsePrice = (priceStr) => {
    if (!priceStr) return 0;
    const match = priceStr.match(/[\d,]+\.?\d*/);
    return match ? parseFloat(match[0].replace(',', '')) : 0;
};

/**
 * Calculate savings percentage
 * @param {number} originalPrice - Original price
 * @param {number} newPrice - New (lower) price
 * @returns {number} Savings percentage
 */
export const calculateSavings = (originalPrice, newPrice) => {
    if (!originalPrice || originalPrice === 0) return 0;
    return ((originalPrice - newPrice) / originalPrice) * 100;
};

/**
 * Format large numbers with commas
 * @param {number} num - Number to format
 * @returns {string} Formatted number
 */
export const formatNumber = (num) => {
    if (!num && num !== 0) return '0';
    return num.toLocaleString();
};
