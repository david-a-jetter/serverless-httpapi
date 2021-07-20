from enum import IntEnum

from pydantic import BaseModel


class Frequency(IntEnum):
    ALMOST_OR_NEVER = 0
    OCCASIONALLY_NOT_SEVERE = 1
    OCCASIONALLY_AND_SEVERE = 2
    FREQUENTLY_NOT_SEVERE = 3
    FREQUENTLY_AND_SEVERE = 4


class Head(BaseModel):
    headaches: Frequency
    faintness: Frequency
    dizziness: Frequency
    insomnia: Frequency


class Eyes(BaseModel):
    watery_itchy: Frequency
    swollen_eyelids: Frequency
    bags_under_eyes: Frequency
    blurred_vision: Frequency


class Ears(BaseModel):
    itchy: Frequency
    aches_infection: Frequency
    drainage: Frequency
    ringing_or_loss: Frequency


class Nose(BaseModel):
    stuffy: Frequency
    sinus_problems: Frequency
    hay_fever: Frequency
    sneezing_attacks: Frequency
    excessive_mucus: Frequency


class MouthThroat(BaseModel):
    chronic_coughing: Frequency
    gagging_or_clearing: Frequency
    sore_hoarse_or_loss: Frequency
    swollen_or_discolored: Frequency
    canker_sores: Frequency


class Skin(BaseModel):
    acne: Frequency
    hives_rash_dry: Frequency
    hair_loss: Frequency
    flushing_hot_flashes: Frequency
    excessive_sweating: Frequency


class Heart(BaseModel):
    irregular: Frequency
    rapid_pounding: Frequency
    chest_pain: Frequency


class Lungs(BaseModel):
    chest_congestion: Frequency
    asthma_bronchitis: Frequency
    shortness_of_breath: Frequency
    difficulty_breathing: Frequency


class DigestiveTract(BaseModel):
    nausea_vomiting: Frequency
    diarrhea: Frequency
    constipation: Frequency
    bloated_feeling: Frequency
    belching_gassy: Frequency
    heartburn: Frequency
    stomach_pain: Frequency


class JointsMuscle(BaseModel):
    joint_pain: Frequency
    arthritis: Frequency
    stiffness: Frequency
    muscle_pain: Frequency
    weakness: Frequency


class Weight(BaseModel):
    binging: Frequency
    craving: Frequency
    excessive_weight: Frequency
    compulsive_eating: Frequency
    water_retention: Frequency
    underweight: Frequency


class EnergyActivity(BaseModel):
    fatigue: Frequency
    apathy: Frequency
    hyperactivity: Frequency
    restlessness: Frequency


class Mind(BaseModel):
    poor_memory: Frequency
    confusion: Frequency
    poor_concentration: Frequency
    poor_physical_coordination: Frequency
    difficulty_making_decisions: Frequency
    stuttering_stammering: Frequency
    slurred_speech: Frequency
    learning_disabilities: Frequency


class Emotions(BaseModel):
    mood_swings: Frequency
    anxiety: Frequency
    anger: Frequency
    depression: Frequency


class Other(BaseModel):
    illness: Frequency
    urgent_urination: Frequency
    genital_itch_discharge: Frequency


class MsqForm(BaseModel):
    hear: Head
    eyes: Eyes
    ears: Ears
    nose: Nose
    mouth_throat: MouthThroat
    skin: Skin
    heart: Heart
    lungs: Lungs
    digestive_tract: DigestiveTract
    joints_muscle: JointsMuscle
    weight: Weight
    energy_activity: EnergyActivity
    mind: Mind
    emotions: Emotions
    other: Other
