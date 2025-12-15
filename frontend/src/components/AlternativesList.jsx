import { motion } from 'framer-motion';
import { TrendingDown, ArrowRight, Sparkles, CheckCircle, XCircle } from 'lucide-react';
import MedicineCard from './MedicineCard';

/**
 * AlternativesList Component
 * 
 * Features:
 * - Reference medicine at top
 * - Alternatives sorted by savings
 * - Large savings badges with pulse
 * - Stagger animation
 * - Total annual savings calculation
 */
const AlternativesList = ({
    referenceMedicine,
    alternatives = [],
    onSelectAlternative,
    onCheckStock,
    onViewDetails
}) => {
    // Calculate total annual savings (assuming 1 tablet/day)
    const calculateAnnualSavings = () => {
        if (!referenceMedicine || alternatives.length === 0) return 0;

        const refPrice = parseFloat(
            (referenceMedicine.price || '0')
                .replace(/[^0-9.]/g, '')
        ) || 0;

        const cheapest = alternatives.reduce((min, alt) => {
            const altPrice = parseFloat(
                (alt.price || '0').replace(/[^0-9.]/g, '')
            ) || 0;
            return altPrice < min ? altPrice : min;
        }, refPrice);

        const dailySavings = refPrice - cheapest;
        return dailySavings * 365;
    };

    const annualSavings = calculateAnnualSavings();

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center gap-3 justify-center text-center">
                <div className="p-3 bg-gradient-to-r from-amber-400 to-orange-500 rounded-xl text-white">
                    <TrendingDown size={28} />
                </div>
                <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                        Save Money - Alternative Brands
                    </h2>
                    <p className="text-gray-500">
                        Found {alternatives.length} cheaper alternatives with the same composition
                    </p>
                </div>
            </div>

            {/* Reference Medicine */}
            {referenceMedicine && (
                <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-5 border-2 border-blue-200"
                >
                    <div className="flex items-center gap-2 text-sm text-blue-600 font-medium mb-3">
                        <Sparkles size={16} />
                        <span>Your Selected Medicine</span>
                    </div>
                    <div className="flex items-center justify-between">
                        <div>
                            <h3 className="text-xl font-bold text-gray-900">
                                {referenceMedicine.name}
                            </h3>
                            <p className="text-gray-500">{referenceMedicine.brand}</p>
                        </div>
                        <div className="text-right">
                            <p className="font-mono text-2xl font-bold text-gray-900">
                                {referenceMedicine.price}
                            </p>
                            <p className="text-sm text-gray-400">Reference Price</p>
                        </div>
                    </div>
                </motion.div>
            )}

            {/* Arrow indicator */}
            <div className="flex justify-center">
                <motion.div
                    animate={{ y: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                    className="p-2 bg-green-100 rounded-full text-green-600"
                >
                    <TrendingDown size={24} />
                </motion.div>
            </div>

            {/* Alternatives Header */}
            <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-gray-700">
                    💡 Cheaper Alternatives:
                </h3>
                {annualSavings > 0 && (
                    <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="px-4 py-2 bg-gradient-to-r from-amber-400 to-orange-500 text-white rounded-full font-bold shadow-lg"
                    >
                        Save up to Rs. {annualSavings.toFixed(0)}/year!
                    </motion.div>
                )}
            </div>

            {/* Alternatives Grid */}
            {alternatives.length > 0 ? (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {alternatives.map((alt, index) => (
                        <motion.div
                            key={alt.name || index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.3, delay: index * 0.1 }}
                            className="relative"
                        >
                            {/* Rank Badge */}
                            <div className="absolute -top-2 -left-2 z-10 w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-lg">
                                {index + 1}
                            </div>

                            <MedicineCard
                                medicine={alt}
                                showSavings={true}
                                savingsPercent={alt.savings_percent || 0}
                                onViewDetails={onViewDetails}
                                onCheckStock={onCheckStock}
                                index={index}
                            />

                            {/* Select Button */}
                            <button
                                onClick={() => onSelectAlternative?.(alt)}
                                className="w-full mt-3 py-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg font-semibold flex items-center justify-center gap-2 hover:shadow-lg hover:scale-[1.02] transition-all"
                            >
                                <CheckCircle size={18} />
                                Select This Alternative
                            </button>
                        </motion.div>
                    ))}
                </div>
            ) : (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-center py-12 bg-gray-50 rounded-xl"
                >
                    <XCircle className="mx-auto text-gray-300 mb-4" size={48} />
                    <h3 className="text-lg font-medium text-gray-600 mb-2">
                        No alternatives found
                    </h3>
                    <p className="text-gray-400">
                        This might be the only brand available for this composition.
                    </p>
                </motion.div>
            )}

            {/* Summary Footer */}
            {alternatives.length > 0 && annualSavings > 0 && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl p-6 text-white text-center"
                >
                    <h3 className="text-2xl font-bold mb-2">
                        💰 Total Potential Savings
                    </h3>
                    <p className="text-4xl font-mono font-bold mb-2">
                        Rs. {annualSavings.toFixed(0)} / year
                    </p>
                    <p className="text-green-100">
                        By switching to the cheapest alternative (1 tablet/day)
                    </p>
                </motion.div>
            )}
        </div>
    );
};

export default AlternativesList;
