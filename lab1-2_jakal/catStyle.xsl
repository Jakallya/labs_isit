<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="utf-8" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <title>Список котиков</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f9f9f9;
                        padding: 20px;
                    }
                    .catList {
                        display: block;
                        width: 40%;
                        margin-bottom: 20px;
                        padding: 15px;
                        background: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    .head {
                        display: block;
                        width: 50%;
                        padding: 10px;
                        margin-bottom: 10px;
                        border-left: 5px solid #FFC0CB;
                        border-radius: 5px;
                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.05);
                        background-color: #ffffff;
                    }
                    .title {
                        font-size: 18px;
                        font-weight: bold;
                        color: #343a40;
                        display: block;
                        margin-bottom: 5px;
                    }
                    .composition {
                        font-style: italic;
                        font-size: 16px;
                        color: #000000;
                        display: block;
                        margin-bottom: 5px;
                    }
                    .characteristics {
                        font-size: 14px;
                        color: #000000;
                        font-weight: bold;
                        display: block;
                    }
                    .header {
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #2c3e50;
                        margin-bottom: 20px;
                    }
                    .image {
                        display: block;
                        width: 100%;
                        max-width: 200px;
                        height: auto;
                        margin-bottom: 10px;
                        border-radius: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <xsl:value-of select="root/header/title"/>
                </div>
                <xsl:for-each select="root/catList">
                    <div class="catList">
                        <div class="head">
                            <span class="title">
                                <xsl:value-of select="head/title"/>
                            </span>
                            <span class="age">
                                Возраст: <xsl:value-of select="head/age"/>
                            </span>
                            <br/>
                            <span class="cuteLevel">
                                Уровень милоты: <xsl:value-of select="head/cuteLevel"/>
                            </span>
                        </div>
                        <img class="image" src="{image}" alt="Котик"/>
                        <div class="composition">
                            <xsl:for-each select="composition/characteristics">
                                <span class="characteristics">
                                    <xsl:value-of select="."/>
                                </span>
                            </xsl:for-each>
                        </div>
                    </div>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>