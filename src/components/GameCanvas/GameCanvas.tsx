import React from 'react';
import css from "./styles/styles.module.css"
import Tile from '../Tile/Tile';

interface GameCanvasProps {
    gridSize: number,
    playerPosition: number
}

const GameCanvas:React.FC<GameCanvasProps> = ({gridSize, playerPosition}) => {
    return (
        <div className={css.wrapper}>
            {Array.from({length: gridSize}, (_, index) => {
                return <Tile playerPosition={playerPosition} index={index} />
            })}
        </div>
    )
}

export default GameCanvas