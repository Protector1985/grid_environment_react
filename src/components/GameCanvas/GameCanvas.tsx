import React from 'react';
import css from "./styles/styles.module.css"
import Tile from '../Tile/Tile';

interface GameCanvasProps {
    gridSize: number,
    playerPosition: number,
    playerDirection: "LEFT" | "RIGHT" | "UP" | "DOWN";
}

const GameCanvas:React.FC<GameCanvasProps> = ({playerDirection, gridSize, playerPosition}) => {
    return (
        <div className={css.wrapper}>
            {Array.from({length: gridSize}, (_, index) => {
                return <Tile playerDirection={playerDirection} playerPosition={playerPosition} index={index} />
            })}
        </div>
    )
}

export default GameCanvas