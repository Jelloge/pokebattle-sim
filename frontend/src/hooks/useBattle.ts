import { useState, useCallback, useRef } from 'react';
import { startBattle, executeMove } from '../api/battleApi';
import type { BattlePokemon, BattleMoveResponse, BattleEvent } from '../api/types';

export type AnimationPhase = 'idle' | 'animating';

export interface BattleState {
  battleId: string | null;
  player: BattlePokemon | null;
  opponent: BattlePokemon | null;
  events: BattleEvent[];
  allEvents: BattleEvent[];
  turnNumber: number;
  battleOver: boolean;
  winner: string | null;
  animationPhase: AnimationPhase;
  loading: boolean;
  playerAnimation: string;
  opponentAnimation: string;
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function useBattle() {
  const [state, setState] = useState<BattleState>({
    battleId: null,
    player: null,
    opponent: null,
    events: [],
    allEvents: [],
    turnNumber: 0,
    battleOver: false,
    winner: null,
    animationPhase: 'idle',
    loading: false,
    playerAnimation: '',
    opponentAnimation: '',
  });
  const animatingRef = useRef(false);
  const battleIdRef = useRef<string | null>(null);

  const initBattle = useCallback(async (pokemonName: string, selectedMoves: string[]) => {
    setState((s) => ({ ...s, loading: true }));
    try {
      const res = await startBattle(pokemonName, selectedMoves);
      battleIdRef.current = res.battleId;
      setState({
        battleId: res.battleId,
        player: res.player,
        opponent: res.opponent,
        events: [],
        allEvents: [],
        turnNumber: 0,
        battleOver: false,
        winner: null,
        animationPhase: 'idle',
        loading: false,
        playerAnimation: '',
        opponentAnimation: '',
      });
    } catch {
      setState((s) => ({ ...s, loading: false }));
    }
  }, []);

  const playTurn = useCallback(async (moveName: string) => {
    const bid = battleIdRef.current;
    if (!bid || animatingRef.current) return;
    animatingRef.current = true;
    setState((s) => {
      if (s.battleOver) return s;
      return { ...s, animationPhase: 'animating' };
    });

    try {
      const res: BattleMoveResponse = await executeMove(bid, moveName);

      // Animate events sequentially
      for (const event of res.events) {
        setState((s) => ({
          ...s,
          events: [...s.events, event],
          allEvents: [...s.allEvents, event],
        }));

        // Drive sprite animations based on event type
        if (event.type === 'move_use') {
          const isPlayer = event.actor === 'player';
          setState((s) => ({
            ...s,
            playerAnimation: isPlayer ? 'sprite-attacking' : '',
            opponentAnimation: isPlayer ? '' : 'sprite-attacking-left',
          }));
          await delay(500);
          setState((s) => ({ ...s, playerAnimation: '', opponentAnimation: '' }));
        } else if (event.type === 'damage' || event.type === 'status_effect') {
          const dmgActor = event.data?.damage ? (event.actor === 'player' ? 'opponent' : 'player') : null;
          if (dmgActor === 'player') {
            setState((s) => ({ ...s, playerAnimation: 'sprite-damaged' }));
          } else if (dmgActor === 'opponent') {
            setState((s) => ({ ...s, opponentAnimation: 'sprite-damaged' }));
          }
          await delay(400);
          setState((s) => ({ ...s, playerAnimation: '', opponentAnimation: '' }));
        } else if (event.type === 'effectiveness' && event.data?.effectiveness === 'super') {
          const target = event.actor === 'player' ? 'opponent' : 'player';
          if (target === 'player') {
            setState((s) => ({ ...s, playerAnimation: 'sprite-super-effective' }));
          } else {
            setState((s) => ({ ...s, opponentAnimation: 'sprite-super-effective' }));
          }
          await delay(600);
          setState((s) => ({ ...s, playerAnimation: '', opponentAnimation: '' }));
        } else if (event.type === 'faint') {
          if (event.actor === 'player') {
            setState((s) => ({ ...s, playerAnimation: 'sprite-fainted' }));
          } else {
            setState((s) => ({ ...s, opponentAnimation: 'sprite-fainted' }));
          }
          await delay(800);
        } else {
          await delay(300);
        }
      }

      // Update final state
      setState((s) => ({
        ...s,
        turnNumber: res.turnNumber,
        player: s.player
          ? {
              ...s.player,
              currentHp: res.player.currentHp,
              statusEffects: res.player.statusEffects,
            }
          : null,
        opponent: s.opponent
          ? {
              ...s.opponent,
              currentHp: res.opponent.currentHp,
              statusEffects: res.opponent.statusEffects,
            }
          : null,
        battleOver: res.battleOver,
        winner: res.winner,
        animationPhase: 'idle',
      }));
    } catch {
      setState((s) => ({ ...s, animationPhase: 'idle' }));
    } finally {
      animatingRef.current = false;
    }
  }, []);

  const loadFromState = useCallback((battleId: string, player: BattlePokemon, opponent: BattlePokemon) => {
    battleIdRef.current = battleId;
    setState({
      battleId,
      player,
      opponent,
      events: [],
      allEvents: [],
      turnNumber: 0,
      battleOver: false,
      winner: null,
      animationPhase: 'idle',
      loading: false,
      playerAnimation: '',
      opponentAnimation: '',
    });
  }, []);

  return { state, initBattle, loadFromState, playTurn };
}
