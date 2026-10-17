import React from 'react';
import {Composition} from 'remotion';
import {EvidenceMotion} from './evidence';
export const Root:React.FC=()=> <Composition id="EvidenceMotion" component={EvidenceMotion} width={1920} height={1080} fps={30} durationInFrames={210} defaultProps={{backgroundVideo:'',files:42000,plots:6000}} />;
