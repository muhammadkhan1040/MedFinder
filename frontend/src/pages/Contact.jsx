import { motion } from 'framer-motion';
import { Mail, MapPin, GraduationCap, Users } from 'lucide-react';

const Contact = () => {
    return (
        <div className="min-h-screen">
            {/* Hero Section with Gradient */}
            <section className="relative min-h-[40vh] flex items-center justify-center overflow-hidden">
                {/* Gradient Background */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 via-purple-600 to-violet-700" />

                {/* Animated background shapes */}
                <div className="absolute inset-0 overflow-hidden">
                    <motion.div
                        animate={{
                            x: [0, 100, 0],
                            y: [0, -50, 0],
                            scale: [1, 1.2, 1]
                        }}
                        transition={{ duration: 20, repeat: Infinity }}
                        className="absolute top-20 left-20 w-64 h-64 bg-white/10 rounded-full blur-3xl"
                    />
                    <motion.div
                        animate={{
                            x: [0, -80, 0],
                            y: [0, 80, 0],
                            scale: [1.2, 1, 1.2]
                        }}
                        transition={{ duration: 25, repeat: Infinity }}
                        className="absolute bottom-20 right-20 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl"
                    />
                </div>

                {/* Content */}
                <div className="relative z-10 text-center px-4">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-4">
                            Meet the Team
                        </h1>
                        <p className="text-xl text-white/80 max-w-2xl mx-auto">
                            NUCES FAST Islamabad | Gen-AI Project 2025
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Team Section */}
            <section className="py-8 px-8 md:px-16 bg-gradient-to-b from-purple-50 to-white flex-grow">
                <div className="max-w-6xl mx-auto">
                    {/* Section Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-16 mx-auto"
                    >
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 text-center">
                            Project Team
                        </h2>
                        <p className="text-gray-600 text-lg text-center">
                            MedFinder - Medicine Availability & Price Comparison System
                        </p>
                    </motion.div>

                    {/* Team Cards Container - Flexbox Layout */}
                    <div className="flex flex-col md:flex-row justify-center items-center gap-8 md:gap-24 px-4">
                        {/* Ubaida Tariq Card */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.1 }}
                            className="w-80 bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 border border-gray-100"
                        >
                            <div className="flex flex-col items-center text-center">
                                {/* Avatar */}
                                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-3xl mb-6 shadow-lg mx-auto">
                                    UT
                                </div>

                                {/* Name & Details */}
                                <h3 className="text-2xl font-bold text-gray-900 mb-2 text-center">
                                    Ubaida Tariq
                                </h3>
                                <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-full mb-4 mx-auto">
                                    <GraduationCap size={18} className="text-blue-600" />
                                    <span className="text-blue-700 font-semibold text-center">22i-1155</span>
                                </div>

                                <p className="text-gray-600 mb-6 text-lg text-center">
                                    Lead Developer
                                </p>

                                {/* Email */}
                                <div className="w-full">
                                    <div className="flex items-center justify-center gap-2 p-4 bg-gray-50 rounded-xl hover:bg-blue-50 transition-colors group">
                                        <Mail size={20} className="text-purple-600 group-hover:text-purple-700 transition-colors" />
                                        <a
                                            href="mailto:i221155@nu.edu.pk"
                                            className="text-purple-600 font-medium hover:text-purple-700 hover:underline transition-colors text-center"
                                        >
                                            i221155@nu.edu.pk
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </motion.div>

                        {/* Muhammad Khan Card */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: 0.2 }}
                            className="w-80 bg-white/80 backdrop-blur-sm rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 border border-gray-100"
                        >
                            <div className="flex flex-col items-center text-center">
                                {/* Avatar */}
                                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-white font-bold text-3xl mb-6 shadow-lg mx-auto">
                                    MK
                                </div>

                                {/* Name & Details */}
                                <h3 className="text-2xl font-bold text-gray-900 mb-2 text-center">
                                    Muhammad Khan
                                </h3>
                                <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-50 rounded-full mb-4 mx-auto">
                                    <GraduationCap size={18} className="text-purple-600" />
                                    <span className="text-purple-700 font-semibold text-center">22i-1040</span>
                                </div>

                                <p className="text-gray-600 mb-6 text-lg text-center">
                                    Frontend Developer
                                </p>

                                {/* Email */}
                                <div className="w-full">
                                    <div className="flex items-center justify-center gap-2 p-4 bg-gray-50 rounded-xl hover:bg-purple-50 transition-colors group">
                                        <Mail size={20} className="text-purple-600 group-hover:text-purple-700 transition-colors" />
                                        <a
                                            href="mailto:i221040@nu.edu.pk"
                                            className="text-purple-600 font-medium hover:text-purple-700 hover:underline transition-colors text-center"
                                        >
                                            i221040@nu.edu.pk
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    </div>

                    {/* Institution Info - Footer Style */}
                    <div className="mt-16 text-center pb-8 mx-auto">
                        <p className="text-gray-900 font-semibold text-lg mb-2 text-center">
                            National University of Computer and Emerging Sciences
                        </p>
                        <p className="text-gray-600 text-sm text-center">
                            FAST Islamabad Campus | December 2025
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Contact;
