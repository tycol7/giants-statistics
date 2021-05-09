module.exports = {
    plugins: [
        {
            resolve: 'gatsby-source-filesystem',
            options: {
                name: 'baseball_data',
                path: 'data'
            }
        },
        `gatsby-transformer-csv`,
        `gatsby-plugin-image`,
        `gatsby-plugin-sharp`,
        `gatsby-transformer-sharp`
    ]
}