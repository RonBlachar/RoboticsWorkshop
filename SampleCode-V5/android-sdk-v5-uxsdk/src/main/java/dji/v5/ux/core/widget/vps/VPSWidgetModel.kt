/*
 * Copyright (c) 2018-2020 DJI
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

package dji.v5.ux.core.widget.vps

import dji.sdk.keyvalue.key.FlightAssistantKey
import dji.sdk.keyvalue.key.FlightControllerKey
import dji.sdk.keyvalue.key.KeyTools
import dji.v5.ux.core.base.DJISDKModel
import dji.v5.ux.core.base.WidgetModel
import dji.v5.ux.core.communication.GlobalPreferenceKeys
import dji.v5.ux.core.communication.GlobalPreferencesInterface
import dji.v5.ux.core.communication.ObservableInMemoryKeyedStore
import dji.v5.ux.core.extension.toDistance
import dji.v5.ux.core.util.DataProcessor
import dji.v5.ux.core.util.UnitConversionUtil
import io.reactivex.rxjava3.core.Flowable

/**
 * Widget Model for the [VPSWidget] used to define
 * the underlying logic and communication
 */
class VPSWidgetModel(
    djiSdkModel: DJISDKModel,
    keyedStore: ObservableInMemoryKeyedStore,
    private val preferencesManager: GlobalPreferencesInterface?
) : WidgetModel(djiSdkModel, keyedStore) {

    private val unitTypeDataProcessor: DataProcessor<UnitConversionUtil.UnitType> = DataProcessor.create(UnitConversionUtil.UnitType.METRIC)
    private val visionPositioningEnabledProcessor: DataProcessor<Boolean> = DataProcessor.create(false)
    private val ultrasonicBeingUsedProcessor: DataProcessor<Boolean> = DataProcessor.create(false)
    private val rawUltrasonicHeightProcessor: DataProcessor<Int> = DataProcessor.create(0)
    private val vpsStateProcessor: DataProcessor<VPSState> = DataProcessor.create(VPSState.ProductDisconnected)

    /**
     * Get the current VPS state
     */
    val vpsState: Flowable<VPSState>
        get() = vpsStateProcessor.toFlowable()

    override fun inSetup() {
        bindDataProcessor(
            KeyTools.createKey(
                FlightAssistantKey.KeyVisionPositioningEnabled), visionPositioningEnabledProcessor)
        bindDataProcessor(
            KeyTools.createKey(
                FlightControllerKey.KeyIsUltrasonicUsed), ultrasonicBeingUsedProcessor)
        bindDataProcessor(
            KeyTools.createKey(
                FlightControllerKey.KeyUltrasonicHeight), rawUltrasonicHeightProcessor)

        val unitTypeKey = GlobalPreferenceKeys.create(GlobalPreferenceKeys.UNIT_TYPE)
        bindDataProcessor(unitTypeKey, unitTypeDataProcessor)
        preferencesManager?.setUpListener()
        preferencesManager?.let { unitTypeDataProcessor.onNext(it.unitType) }
    }

    override fun updateStates() {
        if (productConnectionProcessor.value) {
            if (ultrasonicBeingUsedProcessor.value
                && visionPositioningEnabledProcessor.value) {
                vpsStateProcessor.onNext(
                    VPSState.Enabled(
                        rawUltrasonicHeightProcessor.value.toFloat().toDistance(unitTypeDataProcessor.value),
                        unitTypeDataProcessor.value
                    )
                )
            } else {
                vpsStateProcessor.onNext(VPSState.Disabled)
            }
        } else {
            vpsStateProcessor.onNext(VPSState.ProductDisconnected)
        }
    }

    override fun inCleanup() {
        preferencesManager?.cleanup()
    }

    /**
     * Class to represent states of VPS
     */
    sealed class VPSState {

        /**
         *  When product is disconnected
         */
        object ProductDisconnected : VPSState()

        /**
         * Vision disabled or ultrasonic is not being used
         */
        object Disabled : VPSState()

        /**
         * Current VPS height
         */
        data class Enabled(val height: Float, val unitType: UnitConversionUtil.UnitType) :
            VPSState()

    }
}