import { StaticImage } from "gatsby-plugin-image"
import React from 'react'

export default function Logo() {
 return (
    <div className="center">
    <StaticImage
        src="../images/giants_logo.png"
        alt="Giants Logo"
        width={250}
    />
   </div>
 )
}